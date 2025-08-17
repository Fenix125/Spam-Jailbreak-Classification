import sys
import typer
from app.logging_conf import configure_logging
from rich.console import Console
from app.agent.builder import build_agent

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
            break

        res = agent_executor.invoke({"input": prompt})

        console.print(f"[bold green]> : {res["output"]} [/bold green]")
if __name__ == "__main__":
    cli()
