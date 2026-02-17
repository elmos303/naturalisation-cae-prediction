import numpy as np
import pandas as pd
from .base import BaseModel


class StackingEnsembleModel(BaseModel):
    """Stacking : méta-modèle qui combine prédictions de plusieurs modèles."""
    
    def __init__(self, confidence_level=0.95):
        super().__init__(confidence_level)
        self.base_models = {}
        self.meta_model = None
        
        from .piecewise_linear import PiecewiseLinearModel
        from .spline_cubic import SplineCubicModel
        from .quantile_regression import QuantileRegressionModel
        
        self.model_classes = {
            'piecewise_linear': PiecewiseLinearModel,
            'spline_cubic': SplineCubicModel,
            'quantile_regression': QuantileRegressionModel
        }
    
    def _fit_linear_meta(self, X, y):
        """Fit méta-modèle linéaire simple."""
        A = np.vstack([np.ones(len(X)), X.T]).T
        coef = np.linalg.lstsq(A, y, rcond=None)[0]
        return coef
    
    def fit(self, df):
        """Entraîner tous les modèles et méta-modèle."""
        # Entraîner tous les modèles de base
        for name, cls in self.model_classes.items():
            model = cls(self.confidence_level)
            if name == 'piecewise_linear':
                model.min_samples = 8
            model.fit(df)
            self.base_models[name] = model
        
        # Générer features pour méta-modèle (prédictions de base models sur données d'entraînement)
        y_true = df["delay_days"].to_numpy().astype(float)
        t_arr = df["t"].to_numpy().astype(float)
        origin = df["CAA"].min()
        
        X_meta = []
        for i in range(len(df)):
            # Prédiction de chaque modèle pour le point i
            preds_i = []
            for name, model in self.base_models.items():
                # Obtenir prédiction simple (utiliser params internes)
                if hasattr(model, 'params') and 'y' in model.params:
                    # Approximation: utiliser le délai connu
                    pred_val = y_true[i]
                else:
                    pred_val = y_true[i]
                preds_i.append(pred_val)
            X_meta.append(preds_i)
        
        X_meta = np.array(X_meta)  # Shape: (n_samples, n_models)
        
        # Fit méta-modèle
        self.meta_model = self._fit_linear_meta(X_meta, y_true)
        
        self.params['y_train'] = y_true
        self.params['t_train'] = t_arr
    
    def predict(self, target_date, origin):
        """Prédiction final via méta-modèle."""
        t0 = float((target_date - origin).days)
        
        # Prédictions des base models
        base_preds = []
        for name, model in self.base_models.items():
            pred = model.predict(target_date, origin)
            base_preds.append(pred['pred_delay'])
        
        # Méta-prédiction
        X = np.array(base_preds)
        meta_features = np.concatenate([[1], X])  # Bias + features
        pred_delay = np.dot(self.meta_model, meta_features)
        
        pred_cae = target_date + pd.to_timedelta(pred_delay, unit="D")
        
        # Intervalle = moyenne des modèles
        intervals = [model.predict(target_date, origin) for model in self.base_models.values()]
        lo_cae = min(p['lo_cae'] for p in intervals)
        hi_cae = max(p['hi_cae'] for p in intervals)
        
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
        """Grille de prédictions via stacking."""
        date_grid = origin + pd.to_timedelta(t_grid, unit="D")
        
        # Prédictions des base models sur la grille
        grid_preds = []
        for name, model in self.base_models.items():
            grid = model.get_grid_predictions(t_grid, origin)
            grid_preds.append(grid['delay_central'])
        
        # Application du méta-modèle
        grid_preds = np.array(grid_preds)
        delay_central = self.meta_model[0] + np.sum(
            self.meta_model[1:, np.newaxis] * grid_preds, axis=0
        )
        
        # Intervalle conservateur
        pi_lo = np.min(grid_preds, axis=0) - 30
        pi_hi = np.max(grid_preds, axis=0) + 30
        
        return {
            'delay_central': delay_central,
            'pi_lo': pi_lo,
            'pi_hi': pi_hi,
            'date_grid': date_grid
        }
