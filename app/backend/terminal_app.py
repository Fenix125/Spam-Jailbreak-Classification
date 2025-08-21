import sys
import typer
from app.backend.logging_conf import configure_logging
from app.backend.agent.builder import build_agent
from rich.console import Console

configure_logging()

cli = typer.Typer(add_completion=False)
console = Console()

@cli.command()
def chat(debug: bool = typer.Option(False, "--debug", "-v", help="Verbose agent logs")):
    console.print(f"[dim]Python:[/dim] {sys.executable}")
    agent_executor = build_agent(debug)
    console.print("[bold green]Agent ready.[/bold green] Type [bold]'exit'[/bold] to quit.")

    while True:
        prompt = typer.prompt("> ")
        if prompt.strip().lower() == "exit":
            console.print("[bold green]> : Goodbye! [/bold green]")
            break

        res = agent_executor.invoke({"input": prompt})

        console.print(f"[bold green]> : {res["output"]} [/bold green]")