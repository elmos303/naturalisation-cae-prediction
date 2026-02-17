from abc import ABC, abstractmethod
import pandas as pd
import numpy as np


class BaseModel(ABC):
    """Classe abstraite pour tous les modèles de prédiction."""
    
    def __init__(self, confidence_level=0.95):
        self.confidence_level = confidence_level
        self.model = None
        self.params = {}
    
    @abstractmethod
    def fit(self, df):
        """Entraîner le modèle sur les données."""
        pass
    
    @abstractmethod
    def predict(self, target_date, origin):
        """Prédire CAE pour une date CAA donnée.
        
        Returns:
            dict avec keys: 'pred_delay', 'pred_cae', 'lo_cae', 'hi_cae'
        """
        pass
    
    @abstractmethod
    def get_grid_predictions(self, t_grid, origin):
        """Obtenir les prédictions pour une grille de temps.
        
        Returns:
            dict avec keys: 'delay_central', 'pi_lo', 'pi_hi'
        """
        pass
