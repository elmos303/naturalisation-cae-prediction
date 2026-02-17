#!/usr/bin/env python
"""
Visualisation : tous les modèles sur un même graphique
Utilise: python visualize_all_models.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from utils import load_config, load_data, get_model


def visualize_all_models():
    """Visualiser tous les modèles ensemble."""
    
    config = load_config("config.json")
    df, origin = load_data(config['data_path'])
    target = pd.to_datetime(config['target_date'], dayfirst=True)
    
    models_config = [
        ('piecewise_linear', '#FF6B6B', '-'),
        ('polynomial_regression', '#4ECDC4', '-'),
        ('spline_cubic', '#45B7D1', '-'),
        ('quantile_regression', '#FFA07A', '-'),
    ]
    
    print("📊 Génération de visualisation multi-modèles...")
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Observations
    ax.scatter(df["CAA"], df["CAE"], s=40, alpha=0.7, color='black', 
               label="Observations", zorder=5)
    
    # Grid de prédictions
    t_grid = np.linspace(df["t"].min(), (target - origin).days, 420)
    date_grid = origin + pd.to_timedelta(t_grid, unit="D")
    
    # Boucle sur les modèles
    for model_name, color, style in models_config:
        print(f"  {model_name}...", end=" ")
        try:
            model = get_model(model_name, confidence_level=config['confidence_level'])
            
            if model_name == 'piecewise_linear':
                model.min_samples = config['breakpoint_min_samples']
            elif model_name == 'polynomial_regression':
                model.degree = 3
            
            model.fit(df)
            grid_pred = model.get_grid_predictions(t_grid, origin)
            
            delay_central = grid_pred['delay_central']
            cae_central = date_grid + pd.to_timedelta(delay_central, unit="D")
            
            # Tracer la courbe
            ax.plot(date_grid, cae_central, color=color, linewidth=2.5,
                   linestyle=style, label=model_name.replace('_', ' ').title(), alpha=0.8)
            
            print("✓")
        except Exception as e:
            print(f"✗ ({str(e)[:30]}...)")
    
    # Ligne cible
    ax.axvline(target, linestyle=":", linewidth=2, color="red", alpha=0.6,
              label=f"CAA cible = {target.strftime('%d/%m/%Y')}")
    
    # Formatting
    ax.set_xlabel("Date CAA", fontsize=11)
    ax.set_ylabel("Date CAE", fontsize=11)
    ax.set_title("Comparaison de modèles — Prédiction de délai CAE", fontsize=13, fontweight='bold')
    
    # Dates
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    plt.setp(ax.get_xticklabels(), rotation=25, ha="right")
    
    ax.yaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.yaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%y"))
    
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left", fontsize=10, framealpha=0.95)
    
    fig.tight_layout()
    plt.savefig("models_comparison.png", dpi=200, bbox_inches='tight')
    print(f"\n💾 Graphique sauvegardé: models_comparison.png")
    plt.show()


if __name__ == "__main__":
    visualize_all_models()
