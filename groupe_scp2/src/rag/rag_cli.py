"""
Commandes CLI RAG — Extension du CLI Kiprix existant.
Ajouter ces commandes dans src/cli.py
"""

import click
from .vectorizer import KiprixVectorizer
from .rag_engine import RAGEngine
from .rag_database import RAGDatabase
from .hybrid_rag import HybridRAGEngine  


@click.group()
def rag():
    """Commandes RAG — Questions sur les données Kiprix."""
    pass


@rag.command("vectorize")
@click.option('--territory', '-t', default=None,
              help='Territoire à vectoriser (mq, gp, re, gf). Défaut: tous.')
@click.option('--clear', is_flag=True,
              help='Vider les embeddings existants avant de vectoriser.')
def vectorize(territory: str, clear: bool):
    """Vectorise les produits Kiprix et les stocke dans pgvector."""
    vectorizer = KiprixVectorizer()

    if clear:
        db = RAGDatabase()
        db.clear_embeddings(territory)
        click.echo("🗑️  Embeddings supprimés.")

    click.echo(f"⚙️  Vectorisation en cours{'  (' + territory + ')' if territory else ''}...")
    count = vectorizer.vectorize(territory=territory)
    click.echo(click.style(f"✓ {count} embeddings créés dans pgvector.", fg='green'))


@rag.command("ask")
@click.argument('question')
@click.option('--territory', '-t', default=None,
              help='Filtrer par territoire (mq, gp, re, gf).')
@click.option('--provider', '-p',
              type=click.Choice(['ollama', 'openai']), default='ollama',
              help='LLM à utiliser.')
@click.option('--model', '-m', default='llama3',
              help='Modèle LLM (ex: llama3, mistral, gpt-4o-mini).')
@click.option('--top-k', default=5,
              help='Nombre de sources à récupérer.')
@click.option('--sources', is_flag=True,
              help='Afficher les sources utilisées.')
def ask(question: str, territory: str, provider: str,
        model: str, top_k: int, sources: bool):
    """Pose une question sur les données Kiprix."""
    engine = HybridRAGEngine(llm_provider=provider, model=model)

    click.echo(f"\n🔍 Question : {question}")
    if territory:
        click.echo(f"📍 Territoire : {territory}")
    click.echo("⏳ Recherche en cours...\n")

    result = engine.ask(question, territory=territory, top_k=top_k)

    click.echo("─" * 60)
    click.echo(click.style("💬 Réponse :", fg='green', bold=True))
    click.echo(result['answer'])
    click.echo(f"\n🤖 Généré par : {result.get('provider', 'N/A')}")

    if sources and result.get('sources'):
        click.echo(click.style("\n📚 Sources utilisées :", fg='blue'))
        for i, src in enumerate(result['sources'], 1):
            score = round(src.get('score', 0) * 100, 1)
            meta = src.get('metadata', {})
            click.echo(f"  {i}. {meta.get('name', '?')} "
                       f"({src.get('territory', '?')}) — "
                       f"similarité {score}%")
    click.echo("─" * 60)


@rag.command("stats")
def stats():
    """Statistiques des embeddings dans pgvector."""
    db = RAGDatabase()
    count = db.count_embeddings()
    click.echo(f"📊 Embeddings stockés : {count}")


@rag.command("interactive")
@click.option('--provider', '-p',
              type=click.Choice(['ollama', 'openai']), default='ollama')
@click.option('--model', '-m', default='llama3')
@click.option('--territory', '-t', default=None)
def interactive(provider: str, model: str, territory: str):
    """Mode interactif — pose plusieurs questions en continu."""
    engine = RAGEngine(llm_provider=provider, model=model)

    click.echo(click.style("\n🤖 RAG Kiprix — Mode interactif", fg='green', bold=True))
    click.echo(f"Provider : {provider} | Modèle : {model}")
    if territory:
        click.echo(f"Territoire : {territory}")
    click.echo("Tape 'quit' ou 'exit' pour quitter.\n")

    while True:
        try:
            question = click.prompt("❓ Question")
            if question.lower() in ('quit', 'exit', 'q'):
                break

            result = engine.ask(question, territory=territory)
            click.echo(f"\n💬 {result['answer']}\n")

        except (KeyboardInterrupt, click.exceptions.Abort):
            break

    click.echo("\nAu revoir ! 👋")
