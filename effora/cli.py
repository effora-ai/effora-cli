import typer
from effora.commands import ml, genai, revenue

app = typer.Typer(
    name="effora",
    help="Effora AI — ML and GenAI for Finance.",
    no_args_is_help=True,
)

app.add_typer(ml.app, name="ml", help="ML for Finance commands.")
app.add_typer(genai.app, name="genai", help="GenAI for Finance commands.")
app.add_typer(revenue.app, name="revenue", help="Revenue recognition commands.")


def main():
    app()