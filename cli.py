import sys
print(sys.executable)


from agent import get_agent
from rich.console import Console
from rich.panel import Panel
import typer


app = typer.Typer(add_completion=False)
console = Console()


@app.command()
def chat(debug: bool = typer.Option(False, "--debug", "-v")):
    agent_executor = get_agent(debug)
    console.print("[bold green]Agent ready.[/bold green] Type exit to quit.")
    while True:
        user = typer.prompt("> ")
        if user.strip().lower() == "exit":
            break
        res = agent_executor.invoke({"input": user})
        console.print(Panel(res.get("output", ""), title="assistant", expand=False))

if __name__ == "__main__":
    app()