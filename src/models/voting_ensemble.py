import numpy as np
import pandas as pd
from .base import BaseModel


class VotingEnsembleModel(BaseModel):
    """Ensemble voting : moyenne pondérée de plusieurs modèles."""
    
    def __init__(self, confidence_level=0.95, weights=None):
        super().__init__(confidence_level)
        self.models = {}
        self.weights = weights or {'piecewise_linear': 0.4, 'spline_cubic': 0.3, 'quantile_regression': 0.3}
        # Import local pour éviter dépendances circulaires
        from .piecewise_linear import PiecewiseLinearModel
        from .spline_cubic import SplineCubicModel
        from .quantile_regression import QuantileRegressionModel
        
        self.model_classes = {
            'piecewise_linear': PiecewiseLinearModel,
            'spline_cubic': SplineCubicModel,
            'quantile_regression': QuantileRegressionModel
        }
    
    def fit(self, df):
        """Entraîner tous les modèles."""
        for name, cls in self.model_classes.items():
            model = cls(self.confidence_level)
            if name == 'piecewise_linear':
                model.min_samples = 8
            model.fit(df)
            self.models[name] = model
        
        self.params['origin'] = None
    
    def predict(self, target_date, origin):
        """Prédictions pondérées de tous les modèles."""
        predictions_delay = []
        predictions_cae = []
        predictions_lo = []
        predictions_hi = []
        
        total_weight = 0
        for name, model in self.models.items():
            pred = model.predict(target_date, origin)
            w = self.weights.get(name, 1/len(self.models))
            
            predictions_delay.append(pred['pred_delay'] * w)
            predictions_cae.append(pred['pred_cae'])
            predictions_lo.append(pred['lo_cae'])
            predictions_hi.append(pred['hi_cae'])
            total_weight += w
        
        # Moyenne pondérée du délai
        pred_delay = sum(predictions_delay) / total_weight
        pred_cae = target_date + pd.to_timedelta(pred_delay, unit="D")
        
        # Intervalle = moyenne des extrêmes
        lo_cae = min(predictions_lo)
        hi_cae = max(predictions_hi)
        
        lo_delay = (lo_cae - target_date).days
        hi_delay = (hi_cae - target_date).days
        
        return {
            'pred_delay': pred_delay,
            'pred_cae': pred_cae,
            'lo_cae': lo_cae,
            'hi_cae': hi_cae,
            'lo_delay': lo_delay,
            'hi_delay': hi_delay
        }
    
    def get_grid_predictions(self, t_grid, origin):
        """Grille de prédictions pondérées."""
        date_grid = origin + pd.to_timedelta(t_grid, unit="D")
        
        delay_central = np.zeros_like(t_grid, dtype=float)
        pi_lo = np.zeros_like(t_grid, dtype=float)
        pi_hi = np.zeros_like(t_grid, dtype=float)
        
        for name, model in self.models.items():
            grid_pred = model.get_grid_predictions(t_grid, origin)
            w = self.weights.get(name, 1/len(self.models))
            
            delay_central += grid_pred['delay_central'] * w
            pi_lo += grid_pred['pi_lo'] * w
            pi_hi += grid_pred['pi_hi'] * w
        
        return {
            'delay_central': delay_central,
            'pi_lo': pi_lo,
            'pi_hi': pi_hi,
            'date_grid': date_grid
        }
