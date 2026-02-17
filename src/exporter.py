"""
Export professionnel des résultats de prédiction
Format TXT avec horodatage — Stockage dans le dossier output/predictions/
"""

import os
from datetime import datetime


class ResultsExporter:
    """Export professionnel des résultats de prédiction (TXT uniquement)."""
    
    def __init__(self, model_name, config, df, origin, target, prediction):
        self.model_name = model_name
        self.config = config
        self.df = df
        self.origin = origin
        self.target = target
        self.pred = prediction
        self.timestamp = datetime.now()
        
        # Créer structure de dossiers
        self.export_dir = os.path.join("output", "predictions")
        os.makedirs(self.export_dir, exist_ok=True)
    
    def _format_delay(self, days):
        """Convertir les jours en format lisible (jours, mois et jours)."""
        total_days = int(days)
        months = total_days // 30
        remaining_days = total_days % 30
        
        if months == 0:
            return f"{total_days} jours"
        elif remaining_days == 0:
            return f"{total_days} jours ({months} mois)"
        else:
            return f"{total_days} jours ({months} mois et {remaining_days} jours)"
    
    def _get_filename(self):
        """Générer nom de fichier horodaté (format: prediction_YYYY-MM-DD_HHMMSS.txt)."""
        date_str = self.timestamp.strftime("%Y-%m-%d")
        time_str = self.timestamp.strftime("%H%M%S")
        return os.path.join(self.export_dir, f"prediction_{date_str}_{time_str}.txt")
    
    def export_txt(self):
        """Exporter en format texte structuré et professionnel."""
        filename = self._get_filename()
        
        content = []
        content.append("=" * 80)
        content.append("RAPPORT DE PREDICTION - NATURALISATION CAE")
        content.append("=" * 80)
        content.append("")
        
        content.append("INFORMATIONS GENERALES")
        content.append("-" * 80)
        content.append(f"Date et heure : {self.timestamp.strftime('%d/%m/%Y %H:%M:%S')}")
        content.append(f"Modele utilise : {self.model_name}")
        content.append(f"Niveau de confiance : 95%")
        content.append("")
        
        content.append("DONNEES D'ENTRAINEMENT")
        content.append("-" * 80)
        content.append(f"Nombre d'observations : {len(self.df)}")
        content.append(f"Periode couverte : {self.df['CAA'].min().strftime('%d/%m/%Y')} a {self.df['CAA'].max().strftime('%d/%m/%Y')}")
        content.append("")
        
        content.append("RESULTAT DE PREDICTION")
        content.append("-" * 80)
        content.append(f"Date CAA cible : {self.target.strftime('%d/%m/%Y')}")
        content.append(f"Date CAE predite : {self.pred['pred_cae'].strftime('%d/%m/%Y')}")
        content.append(f"Delai estime : {self._format_delay(self.pred['pred_delay'])}")
        content.append("")
        
        content.append("INTERVALLE DE CONFIANCE (95%)")
        content.append("-" * 80)
        content.append(f"Limite inferieure : {self.pred['lo_cae'].strftime('%d/%m/%Y')}")
        content.append(f"Limite superieure : {self.pred['hi_cae'].strftime('%d/%m/%Y')}")
        content.append(f"Largeur de l'intervalle : {(self.pred['hi_cae'] - self.pred['lo_cae']).days} jours")
        content.append("")
        
        content.append("=" * 80)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(content))
        
        return filename
    
    def export(self):
        """Exporter (raccourci — utilise export_txt)."""
        return self.export_txt()
