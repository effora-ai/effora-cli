import typer

app = typer.Typer(no_args_is_help=True)

@app.command()
def risk(ticker: str = typer.Argument(..., help="Ticker symbol")):
    """Predict 30-day portfolio VaR for a given ticker."""
    typer.echo(f"[effora ml] risk — coming soon for {ticker}")

@app.command()
def anomaly():
    """Detect anomalies in journal entries."""
    typer.echo("[effora ml] anomaly — coming soon")