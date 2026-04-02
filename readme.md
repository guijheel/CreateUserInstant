Markdown
# 🤖 IG Account Auto-Creator (Headless)

Ce script Python automatisé utilise **Playwright** pour créer des comptes sur Instant Gaming de manière invisible. Il simule un comportement humain pour maximiser les chances de succès tout en restant discret.

---

## 📋 Prérequis

Avant de commencer, assure-toi d'avoir installé :
* **Python 3.8** ou une version supérieure.
* Un éditeur de texte (VS Code, Notepad++, etc.).

---

## 🛠️ Installation et Configuration

### 1. Préparation du dossier
Crée un dossier pour ton projet et place le script `main.py` à l'intérieur.

### 2. Création de l'environnement virtuel (Recommandé)
Ouvre un terminal dans ton dossier et tape :

```bash
# Créer l'environnement
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate

# Activer l'environnement (Mac/Linux)
source venv/bin/activate
3. Installation des dépendances
Une fois l'environnement activé, installe les outils nécessaires :

Bash
pip install playwright playwright-stealth
playwright install chromium
4. Configuration des emails
Crée un fichier nommé emails.txt dans le même dossier. Ajoute tes adresses emails, une par ligne :

Plaintext
monemail1@domaine.com
monemail2@domaine.com
🚀 Utilisation
Pour lancer le bot, assure-toi que ton environnement est activé, puis tape :

Bash
python main.py
Paramètres modifiables dans main.py :
PASSWORD_FIXE : Le mot de passe qui sera attribué à tous tes comptes.

headless=True : Mets-le sur False si tu veux voir le navigateur s'ouvrir et taper tout seul (utile pour le premier test).

attente = 600 : C'est le délai en secondes entre deux créations (10 minutes).

🧠 Fonctionnement du Bot
Lecture : Il récupère la liste des emails dans emails.txt.

Invention : Il choisit aléatoirement un prénom et un nom dans une liste intégrée.

Navigation : Il se rend sur la page d'inscription en mode "Stealth" (furtif).

Simulation Humaine :

Il tape les caractères avec un délai variable (50ms à 150ms).

Il génère une date de naissance aléatoire pour chaque profil.

Il effectue des mouvements de souris avant de valider.

Temporisation : Il attend 10 minutes avant de passer à l'email suivant pour ne pas griller ton adresse IP.

⚠️ Avertissements
IP Ban : Même avec des pauses, créer trop de comptes avec la même IP peut entraîner un blocage temporaire de la part du site.

Qualité des Emails : Les emails de type "Jetables/Temporaires" sont souvent détectés et bloqués par le système de sécurité d'Instant Gaming.

Usage : Ce script est fourni à des fins éducatives. L'automatisation peut être contraire aux Conditions Générales d'Utilisation du site visé.

📂 Structure du Projet
Plaintext
.
├── venv/             # Environnement virtuel Python
├── main.py           # Le script principal
├── emails.txt        # Ta liste d'emails
└── README.md         # Ce fichier d'instructions

---

### Comment créer le fichier .md ?
1. Ouvre le **Bloc-notes** ou ton éditeur de code.
2. Copie tout le texte ci-dessus (du premier `#` jusqu'à la fin).
3. Enregistre le fichier sous le nom `README.md` (choisis bien "Tous les fichiers" dans le type
