import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline
from scipy import stats
import math
from .base import BaseModel


class SplineCubicModel(BaseModel):
    """Interpolation par splines cubiques avec intervalle de prédiction."""
    
    def __init__(self, confidence_level=0.95):
        super().__init__(confidence_level)
        self.spline = None
        self.residuals = None
        self.sigma = None
        self.tcrit = None
    
    def fit(self, df):
        """Fit le modèle spline cubique."""
        t_arr = df["t"].to_numpy().astype(float)
        y = df["delay_days"].to_numpy().astype(float)
        
        # Gérer les doublons en t en ajoutant une petite perturbation
        for i in range(1, len(t_arr)):
            if t_arr[i] <= t_arr[i-1]:
                t_arr[i] = t_arr[i-1] + 0.0001
        
        # Fit spline
        self.spline = CubicSpline(t_arr, y, bc_type='not-a-knot')
        
        # Calcul des résidus pour l'intervalle de prédiction
        y_pred = self.spline(t_arr)
        self.residuals = y - y_pred
        
        # Erreur standard
        n = len(t_arr)
        dof = n - 4  # 4 paramètres pour spline cubique
        sigma2 = np.sum(self.residuals**2) / max(dof, 1)
        self.sigma = math.sqrt(sigma2)
        
        # Valeur critique t
        self.tcrit = stats.t.ppf(0.5 + self.confidence_level/2, max(dof, 1))
        
        self.params['t_arr'] = t_arr
        self.params['y'] = y
        self.params['n'] = n
    
    def predict(self, target_date, origin):
        """Prédire pour une date CAA cible."""
        t0 = float((target_date - origin).days)
        
        # Prédiction ponctuelle
        t_max = max(self.params['t_arr'])
        y_arr = self.params['y']
        
        if t0 <= t_max:
            # Interpolation : utiliser la spline
            try:
                pred_delay = float(self.spline(t0))
                # Vérifier si le résultat est raisonnable
                if abs(pred_delay) > 1000:  # Valeur déraisonnable
                    slope = np.mean(np.diff(y_arr[-3:]) / np.diff(np.diff(self.params['t_arr'][-3:])))
                    pred_delay = y_arr[-1] + slope * (t0 - t_max)
            except:
                pred_delay = y_arr[-1]
        else:
            # Extrapolation linéaire simple (pente des 3 derniers points)
            diff_y = np.diff(y_arr[-3:])
            diff_t = np.diff(self.params['t_arr'][-3:])
            if len(diff_t) > 0 and np.sum(diff_t) > 0:
                slope = np.mean(diff_y / diff_t)
            else:
                slope = 1.0
            pred_delay = y_arr[-1] + slope * (t0 - t_max)
        
        # Limiter les valeurs extrêmes
        pred_delay = np.clip(pred_delay, -30, 500)
        
        pred_cae = target_date + pd.to_timedelta(pred_delay, unit="D")
        
        # Intervalle de prédiction (simplifié)
        se_pred = self.sigma * math.sqrt(1 + 1/self.params['n'])
        lo_delay = np.clip(pred_delay - self.tcrit * se_pred, -30, 500)
        hi_delay = np.clip(pred_delay + self.tcrit * se_pred, -30, 500)
        
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
        
        # Interpoation spline
        delay_central = self.spline(t_grid)
        
        # Limiter les valeurs déraisonnables
        delay_central = np.clip(delay_central, -30, 500)
        
        # Intervalle de prédiction
        se_g = self.sigma * np.sqrt(1 + 1/self.params['n'])
        pi_lo = np.clip(delay_central - self.tcrit * se_g, -30, 500)
        pi_hi = np.clip(delay_central + self.tcrit * se_g, -30, 500)
        
        return {
            'delay_central': delay_central,
            'pi_lo': pi_lo,
            'pi_hi': pi_hi,
            'date_grid': date_grid
        }
