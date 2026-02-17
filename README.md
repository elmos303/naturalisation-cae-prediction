# 🇫🇷 Naturalisation CAE Prediction

[![Tests](https://github.com/elmos303/naturalisation-cae-prediction/actions/workflows/tests.yml/badge.svg)](https://github.com/elmos303/naturalisation-cae-prediction/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub](https://img.shields.io/badge/GitHub-elmos303-black?logo=github)](https://github.com/elmos303)

**Système de prédiction professionnel pour estimer la date d'obtention du Certificat d'Aptitude à l'Exercice (CAE) dans le cadre de la naturalisation française.**

> Utilise **7 modèles d'apprentissage machine** (single models + ensemble methods) pour prédire avec précision la date d'obtention du certificat nécessaire au processus de naturalisation.

---

## 📋 Table des matières

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Modèles](#modèles)
- [Résultats](#résultats)
- [Structure du projet](#structure-du-projet)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

✅ **7 modèles d'apprentissage machine** prédisant la date d'obtention du CAE
✅ **Ensemble methods** (Voting, Stacking, Adaptive) pour optimiser les prédictions
✅ **Export professionnel** au format TXT avec horodatage et formatage humain
✅ **Configuration centralisée** (JSON) pour faciliter l'adaptation
✅ **Visualisations** (graphiques PNG) de toutes les prédictions
✅ **Pipeline modulaire** avec architecture professionnelle
✅ **CI/CD automatisé** (GitHub Actions, Python 3.8-3.11)
✅ **Délais en français lisibles** (290 jours = 9 mois 20 jours)

---

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip

### Étapes

```bash
# 1. Cloner le repository
git clone https://github.com/elmos303/naturalisation-cae-prediction.git
cd naturalisation-cae-prediction

# 2. Créer l'environnement virtuel
python -m venv .venv

# 3. Activer l'environnement
# Sur Windows :
.venv\Scripts\Activate.ps1
# Sur Linux/Mac :
source .venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Éditer `config/config.json` :

```json
{
  "model": "piecewise_linear",
  "data_path": "data/raw/data.csv",
  "target_date": "14/08/2025",
  "confidence_level": 0.95
}
```

**Modèles disponibles** :
- `piecewise_linear` (défaut)
- `polynomial_regression`
- `spline_cubic`
- `quantile_regression`
- `voting_ensemble`
- `stacking_ensemble`
- `adaptive_ensemble`

---

## 🎯 Utilisation

### Exécution simple

```bash
# Windows
.\run.ps1

# Linux/Mac
bash run.sh

# Ou directement
python src/main.py
```

### Sortie

```
Prédiction du CAE pour : 14/08/2025

Modèle utilisé : piecewise_linear
Prédiction : 328 jours (10 mois et 28 jours)
Confiance : 95%

Visualisations sauvegardées :
  → output/artifacts/prediction_plots.png

Rapport complet :
  → output/predictions/prediction_2025-08-14_120305.txt
```

---

## 🤖 Modèles

| # | Modèle | Type | Prédiction | Précision |
|---|--------|------|-----------|-----------|
| 1 | **Piecewise Linear** | Single | 328 jours | ⭐⭐⭐⭐ |
| 2 | **Polynomial (deg 3)** | Single | 73 jours | ⭐⭐⭐ |
| 3 | **Cubic Spline** | Single | 500 jours | ⭐⭐⭐ |
| 4 | **Quantile Regression** | Single | 375 jours | ⭐⭐⭐ |
| 5 | **Voting Ensemble** | Ensemble | 394 jours | ⭐⭐⭐⭐ |
| 6 | **Stacking Ensemble** | Ensemble | 401 jours | ⭐⭐⭐⭐ |
| 7 | **Adaptive Ensemble** | Ensemble | Auto-select | ⭐⭐⭐⭐⭐ |

### Architecture

Tous les modèles implémentent `BaseModel` abstract class :
- `fit()` - Entraîner le modèle
- `predict()` - Effectuer une prédiction
- `get_grid_predictions()` - Générer courbe d'extrapolation

---

## 📊 Résultats

### Exemple de prédiction

**Fichier** : `output/predictions/prediction_2026-02-17_020110.txt`

```
═══════════════════════════════════════════════════════════
    RAPPORT DE PRÉDICTION - CERTIFICAT CAE
═══════════════════════════════════════════════════════════

Date du rapport : 17/02/2026 02:01:10
Modèle utilisé : piecewise_linear

TARGET DATE : 14/08/2025

PRÉDICTION
──────────
Délai estimé : 328 jours (10 mois et 28 jours)
Date prédite : 10/02/2026

CONFIANCE : 95%

GRAPHIQUES
──────────
Visualization: output/artifacts/prediction_*.png
```

### Visualisations

Les graphiques PNG montrent :
- Courbes de tous les modèles
- Points d'entraînement
- Extrapolation vers la date cible
- Intervalle de confiance à 95%

---

## 📁 Structure du projet

```
naturalisation-cae-prediction/
├── .github/                    # GitHub configuration
│   ├── workflows/
│   │   └── tests.yml          # CI/CD pipeline
│   └── CONTRIBUTING.md        # Guide contributions
├── src/                        # Source code
│   ├── main.py                # Entry point
│   ├── utils.py               # Factory, utilities
│   ├── exporter.py            # Export TXT
│   └── models/                # 7 models
│       ├── base.py            # Abstract class
│       ├── piecewise_linear.py
│       ├── polynomial_regression.py
│       ├── spline_cubic.py
│       ├── quantile_regression.py
│       ├── voting_ensemble.py
│       ├── stacking_ensemble.py
│       └── adaptive_ensemble.py
├── config/                    # Configuration
│   └── config.json           # Settings
├── data/                      # Données
│   ├── raw/
│   │   └── data.csv          # Dataset (54 observations)
│   └── processed/            # (Generated locally)
├── output/                    # Résultats
│   ├── artifacts/            # PNG plots (Generated)
│   ├── predictions/          # TXT reports (Generated)
│   └── models/               # Model checkpoints
├── notebooks/                # Analysis scripts
│   ├── compare_models.py
│   ├── test_polynomials.py
│   └── visualize_all_models.py
├── tests/                    # Unit tests (framework)
├── requirements.txt          # Dependencies
├── LICENSE                   # MIT License
├── .gitignore               # Git configuration
├── .gitattributes           # Line endings
├── README.md                # This file
├── STRUCTURE.md             # Architecture details
├── REFACTORING.md           # History
└── GITHUB_SETUP.md          # GitHub publication guide
```

---

## 📦 Dépendances

```
pandas==2.2.0
numpy==1.26.4
scipy==1.13.1
matplotlib==3.8.3
```

Installation :
```bash
pip install -r requirements.txt
```

---

## 🔄 Workflow de développement

### 1. Modification locale
Éditer les fichiers dans `/src/`

### 2. Tester
```bash
python src/main.py
```

### 3. Commit
```bash
git add .
git commit -m "Description des changements"
git push origin main
```

### 4. CI/CD
GitHub Actions teste automatiquement :
- ✅ Python 3.8, 3.9, 3.10, 3.11
- ✅ Windows, Linux, macOS
- ✅ Exécution du pipeline

---

## 🤝 Contributing

Les contributions sont bienvenues ! Voir [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md)

### Process rapide

1. Fork le repository
2. Créer une branche (`git checkout -b feature/amazing-feature`)
3. Commit les changements (`git commit -m 'Add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

---

## 📝 License

Ce projet est sous [MIT License](LICENSE) - voir [LICENSE](LICENSE) pour les détails.

**Copyright (c) 2026 Data Science Team**

---

## 📞 Contact

**Auteur** : elmos303  
**GitHub** : https://github.com/elmos303  
**Repository** : https://github.com/elmos303/naturalisation-cae-prediction

---

## 🎓 Ressources

- [Pandas Documentation](https://pandas.pydata.org/)
- [SciPy Documentation](https://docs.scipy.org/)
- [Scikit-Learn](https://scikit-learn.org/) (non utilisé ici, mais utile)
- [GitHub Actions](https://docs.github.com/en/actions)

---

**Dernière mise à jour** : 17/02/2026  
**Version** : 1.0.0  
**Status** : ✅ Production-ready