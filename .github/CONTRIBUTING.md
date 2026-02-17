# Naturalisation CAE Prediction

Système professionnel de prédiction de la date de CAE (Contrôle à Effectuer) à partir de la date de CAA (Contrôle à Affecter) utilisant plusieurs modèles d'apprentissage statistique.

**Status** : ✅ Production Ready

## 📋 Vue d'ensemble

Ce projet implémente un pipeline de prédiction robuste avec :
- **7 modèles** statistiques et ensemble methods
- **Architecture modulaire** et extensible
- **Export professionnel** TXT horodaté
- **Configuration centralisée** JSON
- **Tests CI/CD** GitHub Actions

### Modèles

| Modèle                | Description                      | Prédiction |
| --------------------- | -------------------------------- | ---------- |
| **Piecewise Linear**  | Régression linéaire par segments | 328 jours  |
| **Polynomial**        | Régression polynomiale (deg 3)   | 74 jours   |
| **Spline Cubic**      | Interpolation par splines        | 500 jours  |
| **Quantile**          | Régression quantile asymétrique  | 375 jours  |
| **Voting Ensemble**   | Moyenne pondérée 3 modèles       | 394 jours  |
| **Stacking Ensemble** | Méta-modèle                      | 401 jours  |
| **Adaptive Ensemble** | Auto-sélection meilleur modèle   | ~500 jours |

## 🚀 Installation

### Prérequis
- Python 3.8+
- Git

### Étapes

```bash
# 1. Cloner le repository
git clone https://github.com/YOUR_USERNAME/naturalisation-cae-prediction.git
cd naturalisation-cae-prediction

# 2. Créer l'environnement virtuel
python -m venv .venv

# 3. Activer l'environnement
# Windows:
.\.venv\Scripts\Activate.ps1
# Linux/Mac:
source .venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Lancer le pipeline
python src/main.py
```

## 📁 Structure

```
naturalisation-cae-prediction/
├── src/                      # Code source
│   ├── main.py              # Pipeline principal
│   ├── utils.py             # Utilitaires (loaders, factory)
│   ├── exporter.py          # Export TXT professionnel
│   └── models/              # 7 modèles de prédiction
├── config/config.json       # Configuration centralisée
├── data/raw/data.csv        # Données brutes (54 observations)
├── output/                  # Résultats générés
│   ├── artifacts/           # Graphiques PNG
│   └── predictions/         # Rapports TXT horodatés
├── notebooks/               # Scripts d'analyse
├── tests/                   # Tests unitaires
├── requirements.txt         # Dépendances
├── .gitignore              # Fichiers ignorés Git
├── .gitattributes          # Normalisation line endings
├── LICENSE                 # MIT License
└── README.md              # Ce fichier
```

## ⚙️ Configuration

Éditez `config/config.json` :

```json
{
  "model": "piecewise_linear",      # Modèle à utiliser
  "target_date": "14/08/2025",      # Date CAA cible (DD/MM/YYYY)
  "confidence_level": 0.95,          # Niveau de confiance (0-1)
  "polynomial_degree": 3             # Degré polynomial (si applicable)
}
```

## 🎯 Utilisation

### Lancer le pipeline complet

```bash
# Directement
python src/main.py

# Ou via scripts
.\run.ps1              # Windows
bash run.sh            # Linux/Mac
```

### Résultats générés

- **Graphique** : `output/artifacts/forecast.png` (visualisation prédiction)
- **Rapport** : `output/predictions/prediction_YYYY-MM-DD_HHMMSS.txt` (horodaté)

### Exemple de rapport

```
================================================================================
RAPPORT DE PREDICTION - NATURALISATION CAE
================================================================================

INFORMATIONS GENERALES
--------------------------------------------------------------------------------
Date et heure : 17/02/2026 01:42:23
Modele utilise : piecewise_linear
Niveau de confiance : 95%

RESULTAT DE PREDICTION
--------------------------------------------------------------------------------
Date CAA cible : 14/08/2025
Date CAE predite : 08/07/2026
Delai estime : 328 jours (10 mois et 28 jours)

INTERVALLE DE CONFIANCE (95%)
--------------------------------------------------------------------------------
Limite inferieure : 10/06/2026
Limite superieure : 04/08/2026
Largeur de l'intervalle : 55 jours
```

## 📊 Données

- **Format** : CSV (CAA, CAE)
- **Observations** : 54 points
- **Plage** : 06/03/2025 → 19/05/2025 (75 jours)
- **Localisation** : `data/raw/data.csv`

## 🔍 Détails Techniques

### Architecture

- **Pattern 1** : Factory pour création dynamique de modèles
- **Pattern 2** : Strategy pour interface commune (BaseModel)
- **Pattern 3** : Template Method pour implémentations spécifiques

### Dépendances

```
pandas>=1.3.0       # Manipulation données
numpy>=1.20.0       # Calculs numériques
scipy>=1.7.0        # Statistiques, splines
matplotlib>=3.4.0   # Visualisation
```

### Performances

Tous les modèles testés sur 54 observations :
- Temps d'entraînement : < 1 seconde
- Temps de prédiction : < 100 ms
- Intervalle de confiance : 95%

## 🧪 Tests

```bash
# Tests unitaires (futur)
pytest

# Tests spécifiques modèles
python notebooks/test_polynomials.py
python notebooks/compare_models.py

# Visualisation multi-modèles
python notebooks/visualize_all_models.py
```

## 📚 Documentation

- [README.md](README.md) - Guide principal
- [STRUCTURE.md](STRUCTURE.md) - Architecture détaillée
- [REFACTORING.md](REFACTORING.md) - Historique refactoring

## 🔄 CI/CD

GitHub Actions automatise :
- Tests sur Python 3.8 → 3.11
- Tests sur Windows, Linux, macOS
- Vérification dépendances

## 📝 Contribution

Pour contribuer :

1. Fork le repository
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changes (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📋 License

Ce projet est sous [MIT License](LICENSE) - voir le fichier LICENSE pour détails.

## 👤 Auteur

Data Science Team - 2026

## 🙏 Acknowledgementa

- Pandas & NumPy pour les fondations data science
- Sciences statistiques (SciPy)
- Visualisation (Matplotlib)

---

**Questions ?** Ouvrir une issue sur GitHub ou consulter la [documentation complète](STRUCTURE.md).

**Dernière mise à jour** : 17/02/2026
