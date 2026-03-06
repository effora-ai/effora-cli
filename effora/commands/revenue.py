import typer
import json
from pathlib import Path
from datetime import date, timedelta
from typing import Optional
from effora.engine.recognition import recognize as run_recognition
from effora.engine.models import Contract

app = typer.Typer(no_args_is_help=True)


@app.command()
def recognize(
    contract_file: Optional[Path] = typer.Argument(None, help="Path to contract JSON file"),
    price: Optional[float] = typer.Option(None, "--price", help="Total contract value"),
    start: Optional[str] = typer.Option(None, "--start", help="Start date (YYYY-MM-DD)"),
    term: Optional[int] = typer.Option(None, "--term", help="Term in months"),
    output: str = typer.Option("table", "--output", help="Output format: table | json"),
):
    """Recognize revenue for a contract under ASC 606.

    Examples:

        effora revenue recognize contract.json

        effora revenue recognize --price 12000 --start 2026-01-01 --term 12
    """
    if contract_file:
        if not contract_file.exists():
            typer.echo(f"Error: file not found: {contract_file}", err=True)
            raise typer.Exit(1)
        raw = json.loads(contract_file.read_text())
    elif price and start and term:
        start_date = date.fromisoformat(start)
        # calculate end date from term in months
        month = start_date.month - 1 + term
        end_date = start_date.replace(
            year=start_date.year + month // 12,
            month=month % 12 + 1,
            day=1
        ) - timedelta(days=1)
        raw = {
            "contract_id": "cli",
            "customer_id": "cli",
            "currency": "USD",
            "total_value": price,
            "start_date": start,
            "end_date": end_date.isoformat(),
            "performance_obligations": [
                {"name": "Service", "value": price, "recognition_method": "ratable"}
            ]
        }
    else:
        typer.echo("Error: provide a contract file or --price, --start, and --term", err=True)
        raise typer.Exit(1)

    try:
        contract = Contract(**raw)
    except Exception as e:
        typer.echo(f"Error: invalid contract schema — {e}", err=True)
        raise typer.Exit(1)

    schedule = run_recognition(contract)

    if output == "json":
        typer.echo(schedule.model_dump_json(indent=2))
        return

    if output == "csv":
        typer.echo("period,recognized,deferred")
        for entry in schedule.schedule:
            typer.echo(f"{entry.period},{entry.recognized},{entry.deferred}")
        return

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