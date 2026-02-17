import numpy as np
import pandas as pd
import scipy.stats as st
import math
from .base import BaseModel


class PolynomialRegressionModel(BaseModel):
    """Régression polynomiale avec sélection automatique du degré optimal."""
    
    def __init__(self, confidence_level=0.95, degree=3):
        super().__init__(confidence_level)
        self.degree = degree
        self.poly_coef = None
        self.poly_fit = None
        self.sigma = None
        self.tcrit = None
    
    def fit(self, df):
        """Fit polynomial regression."""
        t_arr = df["t"].to_numpy().astype(float)
        y = df["delay_days"].to_numpy().astype(float)
        
        # Fit polynomial
        self.poly_coef = np.polyfit(t_arr, y, self.degree)
        self.poly_fit = np.poly1d(self.poly_coef)
        
        # Prédictions et résidus
        y_pred = self.poly_fit(t_arr)
        residuals = y - y_pred
        
        # Calcul de sigma pour intervalle de prédiction
        n = len(t_arr)
        dof = n - (self.degree + 1)  # degrees of freedom
        sigma2 = np.sum(residuals**2) / max(dof, 1)
        self.sigma = math.sqrt(sigma2)
        
        # Valeur critique t
        self.tcrit = st.t.ppf(0.5 + self.confidence_level/2, max(dof, 1))
        
        self.params['t_arr'] = t_arr
        self.params['y'] = y
        self.params['n'] = n
        self.params['residuals'] = residuals
    
    def predict(self, target_date, origin):
        """Prédire pour une date CAA cible."""
        t0 = float((target_date - origin).days)
        
        # Prédiction ponctuelle
        pred_delay = float(self.poly_fit(t0))
        pred_cae = target_date + pd.to_timedelta(pred_delay, unit="D")
        
        # Intervalle de prédiction (simplifié)
        n = self.params['n']
        t_arr = self.params['t_arr']
        t_mean = t_arr.mean()
        
        # Terme de variance pour extrapolation
        se_pred = self.sigma * math.sqrt(1 + 1/n + (t0 - t_mean)**2 / np.sum((t_arr - t_mean)**2))
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
        
        # Prédictions polynomiales
        delay_central = self.poly_fit(t_grid)
        
        # Intervalle de prédiction
        n = self.params['n']
        t_arr = self.params['t_arr']
        t_mean = t_arr.mean()
        t_var = np.sum((t_arr - t_mean)**2)
        
        se_g = self.sigma * np.sqrt(1 + 1/n + (t_grid - t_mean)**2 / t_var)
        pi_lo = delay_central - self.tcrit * se_g
        pi_hi = delay_central + self.tcrit * se_g
        
        return {
            'delay_central': delay_central,
            'pi_lo': pi_lo,
            'pi_hi': pi_hi,
            'date_grid': date_grid
        }
