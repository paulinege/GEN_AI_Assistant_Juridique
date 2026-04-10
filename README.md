# ⚖️ Assistant Juridique RAG — Code du Travail

Assistant intelligent combinant RAG et Agents pour répondre à des questions juridiques
basées sur les textes du Code du Travail français.

## 📌 Contexte

Projet réalisé dans le cadre du cours IA Générative — Architecture RAG + Agents.  
Le système permet de :
- Répondre à des questions basées sur les PDFs du Code du Travail (RAG)
- Effectuer des calculs juridiques (indemnités, préavis…) via des agents
- Rechercher de la jurisprudence récente sur le web
- Maintenir une conversation contextuelle avec mémoire

---

## 🏗️ Architecture

```
Question utilisateur
        ↓
    [Routeur]
   /    |    \
RAG  Agent  LLM direct
 ↓     ↓
Chroma  Outils
(Code   (calc,
travail) web…)
        ↓
    Réponse
```

---

## 📁 Structure du projet

```
assistant-juridique-rag/
├── data/                        # PDFs du Code du Travail
│   └── .gitkeep
├── notebooks/                   # Développement itératif (Colab/Jupyter)
│   ├── 01_chargement_docs.ipynb
│   ├── 02_splitting.ipynb
│   ├── 03_vectorstore.ipynb
│   ├── 04_retrieval.ipynb
│   ├── 05_agents.ipynb
│   └── 06_chat_final.ipynb
├── src/                         # Code Python production
│   ├── rag_pipeline.py          # Ingestion + retrieval
│   ├── agents.py                # Outils et agents
│   ├── router.py                # Routage RAG / Agent / LLM
│   └── app.py                   # Interface Chainlit
├── chroma_db/                   # Index vectoriel persisté (ignoré par git)
│   └── .gitkeep
├── tests/                       # Tests unitaires
│   └── test_rag.py
├── .env.example                 # Template variables d'environnement
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

### 1. Cloner le repo

```bash
git clone https://github.com/votre-groupe/assistant-juridique-rag.git
cd assistant-juridique-rag
```

### 2. Créer un environnement virtuel

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\Activate.ps1
# Mac/Linux
source .venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer la clé API

```bash
cp .env.example .env
# Éditer .env et ajouter votre clé OpenAI
```

### 5. Ajouter les PDFs du Code du Travail

Déposer vos fichiers `.pdf` dans le dossier `data/`.  
Source recommandée : [Légifrance](https://www.legifrance.gouv.fr)

---

## ▶️ Lancement

### Interface Chainlit

```bash
chainlit run src/app.py -w
```

Puis ouvrir : `http://localhost:8000`

### Sur Google Colab

```python
from google.colab import drive, userdata
drive.mount('/content/drive')
import os
os.environ["OPENAI_API_KEY"] = userdata.get('OPENAI_API_KEY')
```

---

## 🛠️ Stack technique

| Composant | Outil |
|---|---|
| LLM | OpenAI GPT-3.5 / GPT-4 |
| Orchestration | LangChain + LangGraph |
| Embeddings | OpenAIEmbeddings |
| Vector Store | ChromaDB |
| Chargement PDF | PyPDFLoader |
| Agents | LangChain Agents |
| Interface | Chainlit |

---

## 🔧 Outils agents intégrés

1. **Calculatrice juridique** — calcul d'indemnités, préavis, ancienneté
2. **Recherche web** — jurisprudence récente via Tavily/DuckDuckGo
3. **Calendrier légal** — calcul de délais légaux (rupture, congés…)

---

## 📋 Livrables (sujet prof)

- [x] Partie 1 — Pipeline RAG (ingestion, vectorisation, retrieval)
- [x] Partie 2 — Agents & outils (≥ 3 outils)
- [x] Partie 3 — Routage intelligent RAG / Agent / LLM
- [x] Partie 4 — Mémoire conversationnelle + interface Chainlit

---

## 👥 Équipe

| Membre | Branche | Responsabilité |
|---|---|---|
| Membre 1 | `feature/partie1-rag` | Chargement PDFs + vectorisation |
| Membre 2 | `feature/partie2-agents` | Agents & outils |
| Membre 3 | `feature/partie3-interface` | Routeur + Chainlit + mémoire |

---

## 📝 Exemples de questions

> *"Quel est le délai de préavis pour un CDI après 3 ans d'ancienneté ?"*  
> *"Quelles sont les conditions d'un licenciement pour faute grave ?"*  
> *"Calcule l'indemnité de licenciement pour un salaire de 2500€ et 5 ans d'ancienneté."*  
> *"Quelle est la durée maximale légale du travail hebdomadaire ?"*
