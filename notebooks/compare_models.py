#!/usr/bin/env python
"""
Script pour comparer tous les modèles et générer un rapport de comparaison.
Utilise: python compare_models.py
"""

import pandas as pd
import numpy as np
from datetime import datetime
from utils import load_config, load_data, get_model, format_result


def compare_all_models():
    """Comparer tous les modèles disponibles."""
    
    config = load_config("config.json")
    df, origin = load_data(config['data_path'])
    target = pd.to_datetime(config['target_date'], dayfirst=True)
    
    models_to_test = [
        'piecewise_linear',
        'polynomial_regression',
        'spline_cubic',
        'quantile_regression',
        'voting_ensemble',
        'stacking_ensemble',
        'adaptive_ensemble'
    ]
    
    results = []
    
    print("\n" + "="*80)
    print("🔬 COMPARAISON DE TOUS LES MODÈLES")
    print("="*80)
    print(f"Dataset: {len(df)} observations ({df['CAA'].min().strftime('%d/%m/%Y')} → {df['CAA'].max().strftime('%d/%m/%Y')})")
    print(f"Prédiction pour CAA = {target.strftime('%d/%m/%Y')}\n")
    
    for model_name in models_to_test:
        print(f"🤖 {model_name.upper().replace('_', ' ')}...")
        try:
            model = get_model(model_name, confidence_level=config['confidence_level'])
            
            if model_name == 'piecewise_linear':
                model.min_samples = config['breakpoint_min_samples']
            elif model_name == 'polynomial_regression':
                model.degree = 3
            
            model.fit(df)
            pred = model.predict(target, origin)
            
            pred_delay = pred['pred_delay']
            interval_width = (pred['hi_cae'] - pred['lo_cae']).days
            
            results.append({
                'Modèle': model_name.replace('_', ' ').title(),
                'CAE Estimée': pred['pred_cae'].strftime('%d/%m/%Y'),
                'Délai (j)': f"{pred_delay:.0f}",
                'Intervalle': f"[{pred['lo_cae'].strftime('%d/%m')} ; {pred['hi_cae'].strftime('%d/%m')}]",
                'Largeur PI': f"{interval_width} j"
            })
            
            print(f"   ✓ {pred['pred_cae'].strftime('%d/%m/%Y')} (±{interval_width//2}j)\n")
        
        except Exception as e:
            print(f"   ✗ Erreur: {str(e)[:60]}...\n")
    
    # Afficher tableau
    print("\n" + "="*80)
    print("📊 RÉSUMÉ COMPARATIF")
    print("="*80)
    
    results_df = pd.DataFrame(results)
    print(results_df.to_string(index=False))
    
    print("\n" + "="*80)
    print("💡 RECOMMANDATIONS")
    print("="*80)
    print("""
☑️  Production        → adaptive_ensemble (meilleur modèle auto)
☑️  Robustesse       → voting_ensemble (consensus de 3 modèles)
☑️  Interprétabilité → piecewise_linear (changement de tendance visible)
☑️  Flexible         → spline_cubic (courbe lisse)
    """)


if __name__ == "__main__":
    compare_all_models()
