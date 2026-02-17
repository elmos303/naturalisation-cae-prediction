import numpy as np
import pandas as pd
import scipy.stats as st
import math
from .base import BaseModel


class PiecewiseLinearModel(BaseModel):
    """Régression piecewise linéaire avec détection automatique du point de rupture."""
    
    def __init__(self, confidence_level=0.95, min_samples=8):
        super().__init__(confidence_level)
        self.min_samples = min_samples
        self.breakpoint = None
        self.c1 = None  # coefficients avant rupture
        self.c2 = None  # coefficients après rupture
        self.break_date = None
        self.sigma = None
        self.tcrit = None
    
    def _fit_lin(self, x, y):
        """Fit linéaire simple avec LSQ."""
        A = np.vstack([np.ones(len(x)), x]).T
        coef = np.linalg.lstsq(A, y, rcond=None)[0]
        sse = np.sum((y - (A @ coef))**2)
        return coef, sse
    
    def fit(self, df):
        """Fit le modèle piecewise linéaire."""
        t_arr = df["t"].to_numpy()
        y = df["delay_days"].to_numpy().astype(float)
        
        # Trouver le meilleur breakpoint
        best = None
        for bp in range(self.min_samples, len(df) - self.min_samples):
            c1, sse1 = self._fit_lin(t_arr[:bp], y[:bp])
            c2, sse2 = self._fit_lin(t_arr[bp:], y[bp:])
            if best is None or (sse1 + sse2) < best[0]:
                best = (sse1 + sse2, bp, c1, c2)
        
        _, self.breakpoint, self.c1, self.c2 = best
        self.break_date = df.loc[self.breakpoint, "CAA"]
        
        # Calcul de sigma pour l'intervalle de prédiction
        x2 = t_arr[self.breakpoint:]
        y2 = y[self.breakpoint:]
        n = len(x2)
        yhat2 = self.c2[0] + self.c2[1] * x2
        res = y2 - yhat2
        sigma2 = np.sum(res**2) / (n - 2)
        self.sigma = math.sqrt(sigma2)
        self.tcrit = st.t.ppf(0.5 + self.confidence_level/2, n - 2)
        
        self.params['n'] = n
        self.params['x_mean'] = x2.mean()
        self.params['Sxx'] = np.sum((x2 - self.params['x_mean'])**2)
        self.params['t_arr'] = t_arr
        self.params['y'] = y
    
    def predict(self, target_date, origin):
        """Prédire pour une date CAA cible."""
        t0 = float((target_date - origin).days)
        
        # Prédiction ponctuelle
        a2, b2 = self.c2
        pred_delay = a2 + b2 * t0
        pred_cae = target_date + pd.to_timedelta(pred_delay, unit="D")
        
        # Intervalle de prédiction
        n = self.params['n']
        x_mean = self.params['x_mean']
        Sxx = self.params['Sxx']
        
        se_pred = self.sigma * math.sqrt(1 + 1/n + (t0 - x_mean)**2 / Sxx)
        lo_delay = pred_delay - self.tcrit * se_pred
        hi_delay = pred_delay + self.tcrit * se_pred
        
        lo_cae = target_date + pd.to_timedelta(lo_delay, unit="D")
        hi_cae = target_date + pd.to_timedelta(hi_delay, unit="D")
        
        return {
            'pred_delay': pred_delay,
            'pred_cae': pred_cae,
            'lo_cae': lo_cae,
            'hi_cae': hi_cae,
            'lo_delay': lo_delay,
            'hi_delay': hi_delay
        }
    
    def get_grid_predictions(self, t_grid, origin):
        """Prédictions sur une grille de temps."""
        date_grid = origin + pd.to_timedelta(t_grid, unit="D")
        t_arr = self.params['t_arr']
        
        # Segment central (piecewise)
        delay_central = np.where(
            t_grid < t_arr[self.breakpoint],
            self.c1[0] + self.c1[1] * t_grid,
            self.c2[0] + self.c2[1] * t_grid
        )
        
        # Intervalle sur le segment final
        n = self.params['n']
        x_mean = self.params['x_mean']
        Sxx = self.params['Sxx']
        
        se_grid = self.sigma * np.sqrt(1 + 1/n + (t_grid - x_mean)**2 / Sxx)
        pi_lo = delay_central - self.tcrit * se_grid
        pi_hi = delay_central + self.tcrit * se_grid
        
        return {
            'delay_central': delay_central,
            'pi_lo': pi_lo,
            'pi_hi': pi_hi,
            'date_grid': date_grid
        }
