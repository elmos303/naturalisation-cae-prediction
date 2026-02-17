"""
Utilitaires pour le projet Naturalisation CAE Prediction
"""

import json
import pandas as pd
import sys
import os

# Import absolus pour compatibilité
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import (
    PiecewiseLinearModel, 
    SplineCubicModel, 
    QuantileRegressionModel,
    PolynomialRegressionModel,
    VotingEnsembleModel,
    StackingEnsembleModel,
    AdaptiveEnsembleModel
)


def load_config(config_path):
    """Charger la configuration depuis un fichier JSON."""
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_data(data_path):
    """Charger et préparer les données depuis CSV."""
    df = pd.read_csv(data_path)
    df["CAA"] = pd.to_datetime(df["CAA"], dayfirst=True)
    df["CAE"] = pd.to_datetime(df["CAE"], dayfirst=True)
    df = df.sort_values("CAA").reset_index(drop=True)
    df["delay_days"] = (df["CAE"] - df["CAA"]).dt.days
    
    origin = df["CAA"].min()
    df["t"] = (df["CAA"] - origin).dt.days.astype(float)
    
    return df, origin


def get_model(model_name, **kwargs):
    """Factory pour créer le modèle approprié."""
    models = {
        'piecewise_linear': PiecewiseLinearModel,
        'spline_cubic': SplineCubicModel,
        'quantile_regression': QuantileRegressionModel,
        'polynomial_regression': PolynomialRegressionModel,
        'voting_ensemble': VotingEnsembleModel,
        'stacking_ensemble': StackingEnsembleModel,
        'adaptive_ensemble': AdaptiveEnsembleModel
    }
    
    if model_name not in models:
        raise ValueError(f"Modèle inconnu: {model_name}. Choix: {list(models.keys())}")
    
    return models[model_name](**kwargs)


def format_result(pred_dict, target_date):
    """Formater les résultats pour l'affichage."""
    return {
        'target': target_date.strftime('%d/%m/%Y'),
        'pred_cae': pred_dict['pred_cae'].strftime('%d/%m/%Y'),
        'pred_delay_days': f"{pred_dict['pred_delay']:.0f}",
        'pi_lower': pred_dict['lo_cae'].strftime('%d/%m/%Y'),
        'pi_upper': pred_dict['hi_cae'].strftime('%d/%m/%Y'),
    }
