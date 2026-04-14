# ⚖️ Assistant Juridique RAG — Code du Travail

Assistant intelligent combinant RAG et Agents pour répondre à des questions juridiques
basées sur les textes du Code du Travail français.

## 📌 Contexte

Projet réalisé dans le cadre du cours IA Générative — Architecture RAG + Agents.  
Le système permet de :
- Répondre à des questions basées sur les PDFs du Code du Travail (RAG)
- Effectuer des calculs juridiques (indemnités, préavis…) via un agent calculatrice
- Rechercher de la jurisprudence récente sur le web
- Répondre à des questions sur la météo actuelle
- Suivre l'établissement d'une todo list
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
GEN_AI_Assistant_Juridique/
├── data/                        
│   ├── Contrat_de_travail.pdf
│   ├── Salaires_avantages.pdf
│   ├── Fin_de_contrat.pdf
│   ├── Harcelement.pdf
│   ├── Syndicats.pdf
│   ├── Egalites_professionnelles.pdf
│   └── sécurité_au_travail.pdf
├── notebooks/                   
│   ├── 01_chargement_docs.ipynb  
│   ├── 02_RAG.ipynb              
│   ├── 02_agents_tool.ipynb      
│   └── 03_langchain.ipynb        
├── src/                         
│   ├── __init__.py
│   ├── agent.py                 
│   ├── config.py                
│   ├── rag_pipeline.py          
│   ├── router.py                
│   ├── schemas.py               
│   └── tools.py                 
├── tests/                       
├── app.py                       
├── init_rag.py                  
├── .env.example                 
├── .gitignore
├── LICENSE
├── pytest.ini
├── README.md
└── requirements.txt
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
---

## ▶️ Lancement

### Interface Chainlit

```bash
python -m chainlit run app.py -w
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
| Recherche web | Tavily |
| Météo | OpenWeather API |

---

## 🔧 Outils agents intégrés

1. **Calculatrice juridique** — calcul d'indemnités, préavis, ancienneté
2. **Recherche web** — jurisprudence récente via Tavily/DuckDuckGo
3. **Météo** 
4. **Date du jour**
5. **Todo List**
---
