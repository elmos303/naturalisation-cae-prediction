import numpy as np
import pandas as pd
import math
from .base import BaseModel


class QuantileRegressionModel(BaseModel):
    """Régression quantile pour intervalles de prédiction asymétriques."""
    
    def __init__(self, confidence_level=0.95):
        super().__init__(confidence_level)
        self.coef_median = None
        self.coef_lower = None
        self.coef_upper = None
        self.lower_q = (1 - confidence_level) / 2
        self.upper_q = 1 - self.lower_q
    
    def _fit_quantile(self, x, y, q):
        """Fit régression quantile pour quantile q."""
        # Approche simple : minimiser la perte quantile
        A = np.vstack([np.ones(len(x)), x]).T
        
        def quantile_loss(coef):
            residuals = y - (A @ coef)
            return np.sum(np.where(residuals >= 0, q * residuals, (q - 1) * residuals))
        
        # Fit par moindres carrés pondérés itératifs
        coef = np.linalg.lstsq(A, y, rcond=None)[0]
        
        for _ in range(10):  # 10 itérations
            y_pred = A @ coef
            residuals = y - y_pred
            weights = np.where(residuals >= 0, q, 1 - q)
            weights = np.maximum(weights, 0.01)  # Éviter division par zéro
            
            A_weighted = A * np.sqrt(weights[:, np.newaxis])
            y_weighted = y * np.sqrt(weights)
            
            coef = np.linalg.lstsq(A_weighted, y_weighted, rcond=None)[0]
        
        return coef
    
    def fit(self, df):
        """Fit le modèle quantile."""
        t_arr = df["t"].to_numpy()
        y = df["delay_days"].to_numpy().astype(float)
        
        # Fit trois quantiles
        self.coef_median = self._fit_quantile(t_arr, y, 0.5)
        self.coef_lower = self._fit_quantile(t_arr, y, self.lower_q)
        self.coef_upper = self._fit_quantile(t_arr, y, self.upper_q)
        
        self.params['t_arr'] = t_arr
        self.params['y'] = y
    
    def predict(self, target_date, origin):
        """Prédire pour une date CAA cible."""
        t0 = float((target_date - origin).days)
        
        # Prédictions pour les trois quantiles
        pred_delay = self.coef_median[0] + self.coef_median[1] * t0
        lo_delay = self.coef_lower[0] + self.coef_lower[1] * t0
        hi_delay = self.coef_upper[0] + self.coef_upper[1] * t0
        
        pred_cae = target_date + pd.to_timedelta(pred_delay, unit="D")
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
        
        # Prédictions pour les trois quantiles
        delay_central = self.coef_median[0] + self.coef_median[1] * t_grid
        pi_lo = self.coef_lower[0] + self.coef_lower[1] * t_grid
        pi_hi = self.coef_upper[0] + self.coef_upper[1] * t_grid
        
        return {
            'delay_central': delay_central,
            'pi_lo': pi_lo,
            'pi_hi': pi_hi,
            'date_grid': date_grid
        }
