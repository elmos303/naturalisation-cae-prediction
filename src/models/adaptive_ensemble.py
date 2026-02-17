import numpy as np
import pandas as pd
from .base import BaseModel


class AdaptiveEnsembleModel(BaseModel):
    """Ensemble adaptatif : sélectionne le meilleur modèle selon performance."""
    
    def __init__(self, confidence_level=0.95):
        super().__init__(confidence_level)
        self.models = {}
        self.model_scores = {}
        self.best_model = None
        
        from .piecewise_linear import PiecewiseLinearModel
        from .spline_cubic import SplineCubicModel
        from .quantile_regression import QuantileRegressionModel
        
        self.model_classes = {
            'piecewise_linear': PiecewiseLinearModel,
            'spline_cubic': SplineCubicModel,
            'quantile_regression': QuantileRegressionModel
        }
    
    def _evaluate_model(self, model, y_true, t_arr):
        """Calculer l'erreur du modèle sur l'intervalle d'entraînement."""
        # CV simple : prédire sur les données d'entraînement
        errors = []
        for i in range(len(t_arr)):
            try:
                grid = model.get_grid_predictions(np.array([t_arr[i]]), pd.Timestamp('2020-01-01'))
                pred = grid['delay_central'][0] if hasattr(grid['delay_central'], '__len__') else grid['delay_central']
                error = abs(pred - y_true[i])
                errors.append(error)
            except:
                errors.append(1000)  # Enlever les modèles qui crashent
        
        rmse = np.sqrt(np.mean(np.array(errors)**2))
        return rmse, errors
    
    def fit(self, df):
        """Entraîner tous les modèles et évaluer."""
        y_true = df["delay_days"].to_numpy().astype(float)
        t_arr = df["t"].to_numpy().astype(float)
        
        # Entraîner et évaluer tous les modèles
        for name, cls in self.model_classes.items():
            model = cls(self.confidence_level)
            if name == 'piecewise_linear':
                model.min_samples = 8
            model.fit(df)
            self.models[name] = model
            
            # Évaluer
            rmse, errors = self._evaluate_model(model, y_true, t_arr)
            self.model_scores[name] = {
                'rmse': rmse,
                'errors': errors
            }
        
        # Sélectionner le meilleur
        self.best_model = min(self.model_scores, key=lambda x: self.model_scores[x]['rmse'])
        
        self.params['best_model'] = self.best_model
        self.params['all_models'] = self.models
    
    def predict(self, target_date, origin):
        """Utiliser la prédiction du meilleur modèle."""
        best = self.models[self.best_model]
        return best.predict(target_date, origin)
    
    def get_grid_predictions(self, t_grid, origin):
        """Grille avec le meilleur modèle + alternatives."""
        best = self.models[self.best_model]
        grid_best = best.get_grid_predictions(t_grid, origin)
        
        # Intervalle : enveloppe de tous les modèles pour robustesse
        all_grids = [grid_best['delay_central']]
        for name, model in self.models.items():
            if name != self.best_model:
                grid = model.get_grid_predictions(t_grid, origin)
                all_grids.append(grid['delay_central'])
        
        all_grids = np.array(all_grids)
        
        return {
            'delay_central': grid_best['delay_central'],
            'pi_lo': np.percentile(all_grids, 2.5, axis=0),    # 2.5% quantile
            'pi_hi': np.percentile(all_grids, 97.5, axis=0),   # 97.5% quantile
            'date_grid': grid_best['date_grid']
        }
