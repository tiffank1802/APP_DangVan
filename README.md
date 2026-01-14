# Critère de Dang Van - Analyse de Fatigue
**École Centrale Lyon**

![École Centrale Lyon](https://images.seeklogo.com/logo-png/48/2/ecole-centrale-de-lyon-logo-png_seeklogo-481949.png)

## Description

Cette application web interactive permet d'analyser le comportement en fatigue des matériaux selon le critère de Dang Van. Développée à l'École Centrale Lyon, elle visualise le domaine de sécurité défini par ce critère pour différents types de chargements complexes.

## 🎯 Objectifs

- **Analyse multiaxiale de fatigue** : Appliquer le critère de Dang Van pour prédire l'apparition de fissures
- **Visualisation interactive** : Génération de diagrammes de Dang Van en temps réel
- **Comparaison de chargements** : Étude comparative entre traction-compression et torsion
- **Export de données** : Téléchargement des résultats au format CSV et PNG

## 🧮 Fonctionnalités

### Calcul et Analyse
- **Génération de tenseurs** : Création de tenseurs de contraintes pour différents chargements
- **Calcul de pression hydrostatique** : Détermination de la composante sphérique du tenseur
- **Amplitude de cisaillement maximale** : Recherche du cisaillement maximal sur toutes les facettes
- **Critère de Dang Van** : Application du critère multiaxial de fatigue

### Visualisation
- **Diagrammes interactifs** : Graphiques de pression hydrostatique vs amplitude de cisaillement
- **Personnalisation** : Options de thèmes, de grille et de taille de points
- **Résultats statistiques** : Métriques détaillées sur les calculs effectués

### Export
- **Données brutes** : Export CSV des données de traction-compression et torsion
- **Graphiques** : Téléchargement des diagrammes en haute résolution PNG

## 🚀 Déploiement

Cette application est optimisée pour le déploiement sur **Hugging Face Spaces** avec Gradio.

### Installation locale

```bash
# Cloner le dépôt
git clone <repository-url>
cd APP_DangVan

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python app_gradio.py
```

### Déploiement sur Hugging Face Spaces

1. **Créer un nouvel Espace** sur [Hugging Face](https://huggingface.co/spaces)
2. **Choisir Gradio SDK** 
3. **Uploader les fichiers** du projet
4. **L'application se déploie automatiquement**

## 📋 Structure du projet

```
APP_DangVan/
├── app_gradio.py          # Application Gradio principale
├── versDV.py             # Fonctions de calcul Dang Van
├── deviatoire.py         # Calculs de déviateurs
├── requirements.txt      # Dépendances Python
├── README.md            # Documentation
└── .streamlit/          # Configuration Streamlit (non utilisé pour Gradio)
```

## 👥 Équipe

**Étudiants :**
- Kevin TONGUE
- Paul LORTHIOIR

**Encadrement :**
- Éric FEULVACH
- Françoise FAUVIN

**UE :** Projet de recherche et innovation  
**Thème :** Analyse en fatigue de structures industrielles soumises à des chargements complexes  
**Date :** 2026

## 📚 Théorie du critère de Dang Van

Le critère de Dang Van est un critère multiaxial de fatigue à haute durée de vie qui s'exprime sous la forme :

$$\\tau_{a,max} + \\alpha p_h \\leq \\beta$$

où :
- $\\tau_{a,max}$ est l'amplitude maximale de cisaillement
- $p_h$ est la pression hydrostatique
- $\\alpha$ et $\\beta$ sont des constantes matériau

Ce critère permet de prendre en compte l'effet de la pression hydrostatique sur l'endurance en fatigue des matériaux métalliques.

## 🛠️ Technologies utilisées

- **Python** : Langage de programmation principal
- **Gradio** : Interface web interactive
- **NumPy** : Calculs numériques
- **Matplotlib** : Visualisation graphique
- **SciPy** : Calculs scientifiques avancés
- **Pandas** : Manipulation de données

## 📝 Licence

Projet académique - École Centrale Lyon  
Mécanique des Matériaux | UE: Fatigue et Fissuration  
© 2024 - Tous droits réservés

---

**École Centrale Lyon** | Laboratoire de Mécanique des Matériaux | Projet de recherche et innovation