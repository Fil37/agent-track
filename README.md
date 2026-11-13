# Agent Track

Agent conversationnel local avec un superviseur, un expert spécialisé et des outils.
Le superviseur peut déléguer les questions de musique à l'expert, qui consulte le
flux RSS public d'une chaîne YouTube. Un outil de calcul séparé traite uniquement
des expressions arithmétiques simples et bornées.

## Architecture

```text
Question
   |
   v
Superviseur LangChain
   |----------------------|
   v                      v
Expert musique        Calculatrice sûre
   |
Flux RSS YouTube public
```

Les outils renvoient leurs données ou erreurs explicitement. Le projet n'utilise
pas de clés API ni de scraping de pages privées.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows : .venv\Scripts\activate
python -m pip install -e ".[dev]"
cp .env.example .env
ollama pull llama3.1:8b
```

Définissez `YOUTUBE_CHANNEL_ID` dans `.env` pour activer l'outil RSS. Le modèle
et l'URL Ollama se configurent avec `OLLAMA_MODEL` et `OLLAMA_BASE_URL`.

## Lancer l'agent

```bash
python main.py "Donne-moi les dernières vidéos de cette chaîne"
```

L'agent s'exécute localement avec Ollama. Pour le tester sans appel réseau :

```bash
pytest
```
