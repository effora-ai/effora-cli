import typer

app = typer.Typer(no_args_is_help=True)

@app.command()
def close():
    """Run agentic financial close automation."""
    typer.echo("[effora genai] close — coming soon")

@app.command()
def query(question: str = typer.Argument(..., help="Question to ask against financial documents")):
    """Query financial documents via RAG."""
    typer.echo(f"[effora genai] query — coming soon: '{question}'")