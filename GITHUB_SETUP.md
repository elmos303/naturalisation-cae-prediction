# Guide de Publication sur GitHub

## ✅ Étape 1 : Initialiser Git Localement

```bash
cd c:\Users\elmos\Documents\pref

# Initialiser le repository Git (si pas déjà fait)
git init

# Vérifier le statut
git status
```

## ✅ Étape 2 : Configurer Git (si première utilisation)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Vérifier la config
git config --list
```

## ✅ Étape 3 : Créer le Repository sur GitHub

1. Aller sur https://github.com/new
2. **Repository name** : `naturalisation-cae-prediction`
3. **Description** : `Statistical prediction system for CAE dates from CAA dates using multiple ML models`
4. **Visibility** : Public (ou Private si vous préférez)
5. **Initialize repository** : Laisser vide (on a déjà un local repo)
6. Cliquer **Create repository**

## ✅ Étape 4 : Ajouter les Fichiers et Commit

```bash
# Ajouter tous les fichiers
git add .

# Vérifier ce qui sera commité
git status

# Commit initial
git commit -m "Initial commit: Professional data science project structure

- 7 statistical models for CAE date prediction
- Modular architecture with design patterns
- Professional export system (TXT reports)
- Centralized configuration
- GitHub Actions CI/CD pipeline"
```

## ✅ Étape 5 : Ajouter le Remote et Pousser

```bash
# Remplacer YOUR_USERNAME par votre nom d'utilisateur GitHub
git remote add origin https://github.com/YOUR_USERNAME/naturalisation-cae-prediction.git

# Vérifier le remote
git remote -v

# Renommer la branche en 'main' (GitHub standard)
git branch -M main

# Pousser vers GitHub
git push -u origin main
```

## ✅ Étape 6 : Vérifier sur GitHub

Visiter : `https://github.com/YOUR_USERNAME/naturalisation-cae-prediction`

Vérifier que tout est en place :
- ✅ Code source dans `/src`
- ✅ Configuration dans `/config`
- ✅ Données dans `/data/raw`
- ✅ Documentation (README.md, STRUCTURE.md, etc.)
- ✅ License (MIT)
- ✅ .gitignore et .gitattributes

## ✅ Étape 7 : Activer les Features GitHub

### Activer GitHub Pages (Documentation)
1. Settings → Pages
2. Source : Main branch (si vous voulez héberger la doc)

### Activer GitHub Actions (CI/CD)
1. Actions → Workflows
2. Les tests devraient s'exécuter automatiquement

### Ajouter des Badges (optionnel)
Ajouter au README.md :

```markdown
[![Tests](https://github.com/YOUR_USERNAME/naturalisation-cae-prediction/actions/workflows/tests.yml/badge.svg)](https://github.com/YOUR_USERNAME/naturalisation-cae-prediction/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
```

## 🔄 Workflows Futurs

### Faire un Commit et Push

```bash
# Vérifier les changements
git status

# Ajouter les fichiers modifiés
git add .

# Commit avec message descriptif
git commit -m "Description du changement"

# Pousser vers GitHub
git push
```

### Créer une Nouvelle Branche (pour features)

```bash
# Créer et se placer sur la branche
git checkout -b feature/nom-de-la-feature

# Faire des modifications et commits
git add .
git commit -m "Implement feature: nom-de-la-feature"

# Pousser la branche
git push -u origin feature/nom-de-la-feature

# Sur GitHub : créer une Pull Request
```

### Merger vers Main

```bash
# Passer à main
git checkout main

# Récupérer les derniers changements
git pull origin main

# Merger la branche
git merge feature/nom-de-la-feature

# Pousser
git push
```

## 📋 Checklist Finale

- [ ] Git configuré localement
- [ ] Repository créé sur GitHub
- [ ] Fichiers ajoutés et committés
- [ ] Remote configuré
- [ ] Premier push vers main
- [ ] Code visible sur GitHub
- [ ] .gitignore respecté (pas de .venv/, output/, etc.)
- [ ] License présente
- [ ] README complet
- [ ] GitHub Actions activé
- [ ] Badges ajoutés (optionnel)

## 🆘 Troubleshooting

### "Fatal: 'origin' does not appear to be a git repository"
```bash
git remote add origin https://github.com/YOUR_USERNAME/naturalisation-cae-prediction.git
```

### "Permission denied (publickey)"
```bash
# Générer une SSH key si nécessaire
ssh-keygen -t ed25519 -C "your.email@example.com"

# Ajouter à GitHub Settings → SSH Keys
```

### "Branch main set up to track remote"
```bash
# Ça c'est normal et bon !
```

### Réinitialiser un commit failed
```bash
git reset HEAD~1   # Annuler le dernier commit
git status         # Voir les fichiers
git add .          # Re-ajouter
git commit -m "..."  # Re-committer
```

## 📚 Ressources

- GitHub Docs: https://docs.github.com/
- Git Guide: https://git-scm.com/book
- GitHub Actions: https://docs.github.com/en/actions

---

**Besoin d'aide ?** Consultez les docs officielles ou créez une issue sur le repository !
