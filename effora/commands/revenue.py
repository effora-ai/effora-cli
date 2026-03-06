import typer
import json
from pathlib import Path
from effora.engine import recognize, Contract

app = typer.Typer(no_args_is_help=True)


@app.command()
def recognize(
    contract_file: Path = typer.Argument(..., help="Path to contract JSON file"),
    output: str = typer.Option("table", help="Output format: table | json")
):
    """Recognize revenue for a contract under ASC 606."""
    if not contract_file.exists():
        typer.echo(f"Error: file not found: {contract_file}", err=True)
        raise typer.Exit(1)

    raw = json.loads(contract_file.read_text())

    try:
        contract = Contract(**raw)
    except Exception as e:
        typer.echo(f"Error: invalid contract schema — {e}", err=True)
        raise typer.Exit(1)

    schedule = recognize(contract)

    if output == "json":
        typer.echo(schedule.model_dump_json(indent=2))
        return

    # table output
    typer.echo(f"\nRevenue Schedule — {schedule.contract_id}")
    typer.echo(f"Customer: {schedule.customer_id}  |  Total: {schedule.currency} {schedule.total_value:,.2f}")
    typer.echo("-" * 50)
    typer.echo(f"{'Period':<12} {'Recognized':>14} {'Deferred':>14}")
    typer.echo("-" * 50)
    for entry in schedule.schedule:
        typer.echo(f"{entry.period:<12} {entry.recognized:>14,.2f} {entry.deferred:>14,.2f}")
    typer.echo("-" * 50)
    typer.echo(f"{'Total':<12} {schedule.audit['recognized_total']:>14,.2f}")
    typer.echo(f"\nStandard: {schedule.audit['standard']}  |  Generated: {schedule.audit['generated_at']}\n")