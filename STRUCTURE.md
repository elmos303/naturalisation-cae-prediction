# Structure Professionnelle du Projet

Document expliquant l'organisation des dossiers et fichiers selon les meilleures pratiques data science.

## Hiérarchie des Dossiers

### `/src` - Code Source Principal
**Contient toute la logique applicative**

```
src/
├── __init__.py                    # Package initialization
├── main.py                        # Pipeline principal (orchestration)
├── utils.py                       # Utilitaires (loaders, factory, formatters)
├── exporter.py                    # Export des résultats (TXT professionnel)
└── models/                        # Module des modèles
    ├── __init__.py
    ├── base.py                    # Classe abstraite BaseModel (interface commune)
    │
    ├── piecewise_linear.py        # Régression piecewise linéaire
    ├── polynomial_regression.py    # Régression polynomiale
    ├── spline_cubic.py            # Interpolation par splines cubiques
    ├── quantile_regression.py     # Régression quantile
    │
    ├── voting_ensemble.py         # Combination : moyenne pondérée
    ├── stacking_ensemble.py       # Combination : méta-modèle
    └── adaptive_ensemble.py       # Combination : auto-sélection
```

### `/data` - Gestion des Données
**Données brutes et traitées (séparation data/code)**

```
data/
├── raw/                           # Données d'origine (ne jamais modifier)
│   └── data.csv                   # Données brutes (54 observations CAA/CAE)
└── processed/                     # Données transformées (optionnel pour future)
```

### `/config` - Configuration Centralisée
**Paramètres du système (séparation config/code)**

```
config/
└── config.json                    # Fichier de configuration unique
    ├── model : modèle à utiliser
    ├── data_path : chemin des données
    ├── target_date : date CAA cible
    ├── confidence_level : seuil de confiance
    └── ...autres paramètres
```

### `/output` - Résultats et Artefacts
**Sorties du pipeline (jamais en git)**

```
output/
├── artifacts/                     # Graphiques et visualisations
│   ├── forecast.png               # Prédiction avec observations
│   └── ...autres PNG
│
├── predictions/                   # Rapports horodatés
│   ├── prediction_2026-02-17_014223.txt
│   ├── prediction_2026-02-17_050000.txt
│   └── ...autres TXT (YYYY-MM-DD_HHMMSS)
│
└── models/                        # Modèles sérialisés (futur)
    ├── model_v1.pkl
    └── ...pickle files
```

### `/notebooks` - Scripts d'Analyse
**Utilitaires et scripts de comparaison (non-production)**

```
notebooks/
├── compare_models.py              # Comparaison tous modèles
├── test_polynomials.py            # Teste degrés polynomiaux
└── visualize_all_models.py        # Visualisation multi-modèles
```

### `/tests` - Tests Unitaires
**Suite de tests (futur)**

```
tests/
├── __init__.py
├── test_models.py                 # Tests des modèles
├── test_utils.py                  # Tests utilitaires
└── test_exporter.py               # Tests exporteur
```

## Fichiers Racine

| Fichier            | Rôle                                       |
| ------------------ | ------------------------------------------ |
| `run.ps1`          | Script d'exécution pour Windows PowerShell |
| `run.sh`           | Script d'exécution pour Linux/Mac/Bash     |
| `requirements.txt` | Dépendances Python (pip)                   |
| `.gitignore`       | Fichiers ignorés par Git                   |
| `README.md`        | Documentation principal                    |
| `STRUCTURE.md`     | Ce fichier (documentation d'architecture)  |

## Dossier `.venv`

Environnement virtuel Python isolé du reste du système.

```bash
.venv/
├── Scripts/         # Exécutables Windows (python.exe, pip.exe, Activate.ps1)
├── Lib/             # Packages Python installés
└── pyvenv.cfg      # Configuration de l'environnement
```

## Architecture Logique

### Design Pattern 1 : Factory Pattern
**Utilitaires** : `get_model(model_name)` crée les modèles dynamiquement

```python
# Dans utils.py
def get_model(model_name, **kwargs):
    models = {
        'piecewise_linear': PiecewiseLinearModel,
        'spline_cubic': SplineCubicModel,
        ...
    }
    return models[model_name](**kwargs)
```

### Design Pattern 2 : Strategy Pattern
**BaseModel** : Interface commune pour tous les modèles

```python
class BaseModel(ABC):
    @abstractmethod
    def fit(self, df):
        pass
    
    @abstractmethod
    def predict(self, target_date, origin):
        pass
    
    @abstractmethod
    def get_grid_predictions(self, t_grid, origin):
        pass
```

### Design Pattern 3 : Template Method
**Chaque modèle** : Implémente les 3 methods abstraites

```python
class PiecewiseLinearModel(BaseModel):
    def fit(self, df):
        # Implémentation spécifique
        pass
    
    def predict(self, target_date, origin):
        # Implémentation spécifique
        pass
    
    def get_grid_predictions(self, t_grid, origin):
        # Implémentation spécifique
        pass
```

## Flux de Données

```
┌─────────────────────────────────────────────────────────────┐
│                       MAIN PIPELINE                         │
└─────────────────────────────────────────────────────────────┘

1. Configuration
   └─> config/config.json [(model, target_date, ...)]

2. Chargement des données
   └─> data/raw/data.csv [(CAA dates, CAE dates)]
   └─> utils.load_data() : normalisation + calcul délais

3. Modèle
   └─> src/models/{selected_model}.py
   └─> fit(df) : entraînement
   └─> predict() : prédiction ponctuelle + intervalle

4. Visualisation
   └─> Graphique introspect
   └─> output/artifacts/forecast.png

5. Export
   └─> Rapport formaté professionnel
   └─> output/predictions/prediction_YYYY-MM-DD_HHMMSS.txt
```

## Nommage et Conventions

### Fichiers Python
- `snake_case` (fichiers) : `piecewise_linear.py`, `voting_ensemble.py`
- `PascalCase` (classes) : `PiecewiseLinearModel`, `VotingEnsembleModel`
- `snake_case` (fonctions) : `load_config()`, `get_model()`

### Variables
- `snake_case` : `target_date`, `pred_delay`, `confidence_level`
- Pas d'underscore unique sauf `_` comme "throwaway"
- Préfixe `_` pour private : `_fit_linear()`, `_get_filename()`

### Dates
- Format fichier : `YYYY-MM-DD` (ISO 8601) : `2026-02-17`
- Format affichage : `DD/MM/YYYY` (français) : `17/02/2026`
- Horodatage : `YYYY-MM-DD_HHMMSS` (fichiers) : `2026-02-17_014223`

### Chemins
- Tous les chemins sont relatifs au répertoire racine
- Utility : `os.path.join()` pour compatibilité OS
- Relative imports dans les packages (`from .models import`)

## Dépendances

### Production
```
pandas          # Manipulation et analyse données
numpy           # Calculs numériques
scipy           # Statistiques (t-stat, CubicSpline)
matplotlib      # Visualisation graphiques
```

### Développement (futur)
```
pytest          # Tests unitaires
black           # Formatage code
pylint          # Linting
sphinx          # Documentation
```

## Bonnes Pratiques Appliquées

✅ **Séparation des préoccupations**
- Data ≠ Code
- Config ≠ Code
- Tests ≠ Production

✅ **Composabilité**
- Chaque modèle = classe indépendante
- Interfaces claires via BaseModel
- Factory pattern pour flexibilité

✅ **Maintenabilité**
- Code modulaire et réutilisable
- Imports explicites (pas `import *`)
- Docstrings et commentaires pertinents

✅ **Reproductibilité**
- Requirements.txt
- Config centralisée
- Seeds aléatoires gérés

✅ **Professionnalisme**
- Structure standard data science
- Export structuré TXT
- Documentation complète

## Migration des Anciens Fichiers

Les fichiers anciens restent à la racine pour compatibilité :
- `main.py` (ancien) → `src/main.py` (nouveau)
- `model/` (ancien) → `src/models/` (nouveau)
- `config.json` (ancien) → `config/config.json` (nouveau)
- `data.csv` (ancien) → `data/raw/data.csv` (nouveau)

## Étapes Suivantes (Roadmap)

1. **Tests unitaires** : `/tests` avec pytest
2. **Persistance modèles** : Sérialiser modèles entraînés
3. **API REST** : Flask/FastAPI pour intégration externe
4. **Base de données** : PostgreSQL/SQLite pour historique
5. **Packaging** : Distribuer en PyPI

---

**Version** : 1.0.0
**Date** : 17/02/2026
**Auteur** : Data Science Team
