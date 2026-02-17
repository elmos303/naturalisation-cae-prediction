"""
Script principal - Orchestration du pipeline de prédiction
Naturalisation CAE Prediction v1.0
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Adjust path for imports
src_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, src_dir)

from utils import load_config, load_data, get_model, format_result
from exporter import ResultsExporter


def main():
    """Pipeline principal de prédiction."""
    
    # Charger configuration
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')
    config = load_config(config_path)
    
    # Charger données
    print("📊 Chargement des données...")
    data_path = os.path.join(os.path.dirname(__file__), '..', config['data_path'])
    df, origin = load_data(data_path)
    print(f"   {len(df)} observations de {df['CAA'].min().strftime('%d/%m/%Y')} à {df['CAA'].max().strftime('%d/%m/%Y')}")
    
    # Initialiser et entraîner le modèle
    print(f"🤖 Initialisation du modèle: {config['model']}")
    model = get_model(
        config['model'],
        confidence_level=config['confidence_level']
    )
    
    # Ajouter paramètres spécifiques
    if config['model'] == 'piecewise_linear':
        model.min_samples = config.get('breakpoint_min_samples', 8)
    elif config['model'] == 'polynomial_regression':
        model.degree = config.get('polynomial_degree', 3)
    
    print("   Entraînement en cours...")
    model.fit(df)
    
    # Prédiction pour la date cible
    target = pd.to_datetime(config['target_date'], dayfirst=True)
    print(f"🎯 Prédiction pour CAA = {target.strftime('%d/%m/%Y')}")
    
    pred = model.predict(target, origin)
    result = format_result(pred, target)
    
    print(f"\n   Prédiction ponctuelle: {result['pred_cae']}")
    print(f"   Délai estimé: {result['pred_delay_days']} jours")
    print(f"   Intervalle {config['confidence_level']*100:.0f}%: [{result['pi_lower']} ; {result['pi_upper']}]")
    
    # Afficher le modèle sélectionné si adaptive
    if config['model'] == 'adaptive_ensemble':
        best_model = model.params['best_model']
        print(f"   Meilleur modèle sélectionné: {best_model}")
    
    # Grille de prédictions pour visualisation
    print("\n📈 Génération des prédictions de visualisation...")
    t_grid = np.linspace(df["t"].min(), (target - origin).days, 420)
    grid_pred = model.get_grid_predictions(t_grid, origin)
    
    date_grid = grid_pred['date_grid']
    delay_central = grid_pred['delay_central']
    pi_lo = grid_pred['pi_lo']
    pi_hi = grid_pred['pi_hi']
    
    # Conversion en dates
    cae_central = date_grid + pd.to_timedelta(delay_central, unit="D")
    cae_lo = date_grid + pd.to_timedelta(pi_lo, unit="D")
    cae_hi = date_grid + pd.to_timedelta(pi_hi, unit="D")
    
    # Validation et conversion pour plot
    valid = ~pd.isna(cae_lo) & ~pd.isna(cae_hi)
    x_num = mdates.date2num(date_grid[valid].to_pydatetime())
    lo_num = mdates.date2num(cae_lo[valid].to_pydatetime())
    hi_num = mdates.date2num(cae_hi[valid].to_pydatetime())
    
    # === VISUALIZATION ===
    print("🎨 Création du graphique...")
    fig, ax = plt.subplots(figsize=(12.8, 7.3))
    
    # Observations
    ax.scatter(df["CAA"], df["CAE"], s=32, alpha=0.9, label="Observations (CAA→CAE)")
    
    # Intervalle de prédiction (bande)
    ax.fill_between(x_num, lo_num, hi_num, color="#ff69b4", alpha=0.18,
                    label=f"Intervalle prédictif {config['confidence_level']*100:.0f}%")
    
    # Modèle central (courbe)
    ax.plot(date_grid, cae_central, color="red", linewidth=2.4,
            label=f"Modèle: {config['model'].replace('_', ' ').title()}")
    
    # Ligne cible (date CAA)
    ax.axvline(target, linestyle=":", linewidth=2.3, color="red", alpha=0.95,
               label=f"CAA cible = {target.strftime('%d/%m/%Y')}")
    
    # Point de prédiction (carré rouge) + intervalle
    ax.scatter([target], [pred['pred_cae']], marker="s", s=90, color="red", zorder=6,
               label="Prédiction ponctuelle")
    ax.vlines(target, pred['lo_cae'], pred['hi_cae'], color="red", linewidth=2.2, alpha=0.9, zorder=5)
    
    # Titres et labels
    title = "Naturalisation — Estimation de la date CAE à partir de la date CAA"
    subtitle = (f"Modèle: {config['model'].replace('_', ' ').title()} • "
                f"Données: {df['CAA'].min().strftime('%d/%m/%Y')} → {df['CAA'].max().strftime('%d/%m/%Y')} • "
                f"Extrapolation: CAA={target.strftime('%d/%m/%Y')}")
    ax.set_title(title + "\n" + subtitle, fontsize=14)
    
    ax.set_xlabel("Date CAA (Contrôle à Affecter)")
    ax.set_ylabel("Date CAE (Contrôle à Effectuer)")
    
    # Grille
    ax.grid(True, which="major", linestyle="-", linewidth=0.6, color="0.85")
    ax.grid(True, which="minor", linestyle="-", linewidth=0.35, color="0.92")
    ax.minorticks_on()
    
    # Format dates
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%Y"))
    plt.setp(ax.get_xticklabels(), rotation=25, ha="right")
    
    # Annotation
    txt = (
        f"CAA cible : {target.strftime('%d/%m/%Y')}\n"
        f"CAE estimée : {pred['pred_cae'].strftime('%d/%m/%Y')}\n"
        f"PI {config['confidence_level']*100:.0f}% : [{pred['lo_cae'].strftime('%d/%m/%Y')} ; {pred['hi_cae'].strftime('%d/%m/%Y')}]\n"
        f"Δ estimé : {pred['pred_delay']:.0f} jours"
    )
    ax.annotate(txt, xy=(target, pred['pred_cae']), xytext=(18, -12), textcoords="offset points",
                fontsize=10, bbox=dict(boxstyle="round,pad=0.45", fc="white", ec="0.7", alpha=0.96))
    
    ax.legend(loc="upper left", frameon=True, framealpha=0.96)
    fig.tight_layout()
    
    # Sauvegarder le graphique
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output', 'artifacts')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, config.get('output_filename', 'forecast.png'))
    plt.savefig(output_path, dpi=240)
    print(f"💾 Graphique sauvegardé: {output_path}")
    
    # Exporter résultats
    print("\n📤 Export des résultats...")
    exporter = ResultsExporter(config['model'], config, df, origin, target, pred)
    txt_file = exporter.export()
    print(f"   ✓ Export : {txt_file}")
    
    plt.show()


if __name__ == "__main__":
    main()
