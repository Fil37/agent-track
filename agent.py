"""Supervisor agent and delegated music specialist."""

from langchain.agents import create_agent
from langchain_core.tools import tool

from config import create_chat_model
from tools import calculate, latest_youtube_uploads


def create_supervisor():
    """Create an agent that delegates music questions to a focused expert."""
    model = create_chat_model()
    music_expert = create_agent(
        model,
        [latest_youtube_uploads],
        system_prompt=(
            "Tu es un expert musique. Appelle l'outil RSS pour toute question "
            "sur les dernières vidéos. N'invente jamais de titre, date ou URL."
        ),
    )

    @tool
    def ask_music_expert(question: str) -> str:
        """Delegate a music-related question to the specialist agent."""
        result = music_expert.invoke({"messages": [("user", question)]})
        return str(result["messages"][-1].content)

    return create_agent(
        model,
        [ask_music_expert, calculate],
        system_prompt=(
            "Tu es un superviseur utile et précis. Délègue les questions musicales "
            "à l'expert spécialisé. Utilise la calculatrice pour les opérations. "
            "Ne fabrique jamais de résultat ni de source."
        ),
    )
