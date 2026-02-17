#!/usr/bin/env python
"""
Script pour tester les polynômes de différents degrés.
Utilise: python test_polynomials.py
"""

import pandas as pd
import numpy as np
from utils import load_config, load_data, get_model, format_result


def test_polynomial_degrees():
    """Tester différents degrés de polynomial."""
    
    config = load_config("config.json")
    df, origin = load_data(config['data_path'])
    target = pd.to_datetime(config['target_date'], dayfirst=True)
    
    degrees = [2, 3, 4, 5]
    
    print("\n" + "="*80)
    print("🔬 COMPARAISON - DEGRÉS DE POLYNÔMES")
    print("="*80)
    print(f"Dataset: {len(df)} observations ({df['CAA'].min().strftime('%d/%m/%Y')} → {df['CAA'].max().strftime('%d/%m/%Y')})")
    print(f"Prédiction pour CAA = {target.strftime('%d/%m/%Y')}\n")
    
    results = []
    
    for degree in degrees:
        print(f"🧮 Polynomial Degree {degree}...")
        try:
            model = get_model('polynomial_regression', confidence_level=config['confidence_level'])
            model.degree = degree
            model.fit(df)
            pred = model.predict(target, origin)
            
            pred_delay = pred['pred_delay']
            interval_width = (pred['hi_cae'] - pred['lo_cae']).days
            
            results.append({
                'Degré': degree,
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
    print("📊 RÉSUMÉ - COMPARAISON DEGRÉS")
    print("="*80)
    
    results_df = pd.DataFrame(results)
    print(results_df.to_string(index=False))
    
    print("\n" + "="*80)
    print("💡 INTERPRÉTATION")
    print("="*80)
    print("""
Degré 2 : Parabole (concave/convexe) — Good compromise entre flexibilité et stabilité
Degré 3 : Cubique (S-curve) — Plus flexible, capture plus de non-linéarité
Degré 4 : Quartique — Très flexible, risque d'overfitting
Degré 5  : Très flexible — Très à risque d'overfitting

📌 RECOMMANDATION: Degré 3 est un bon équilibre
    """)


if __name__ == "__main__":
    test_polynomial_degrees()
