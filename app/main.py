from app.config import settings

def main():
    if settings.run_mode == "web":
        import uvicorn
        uvicorn.run("app.web_app:app")
    elif settings.run_mode == "cli":
        from app.terminal_app import cli
        cli()
    else:
        raise SystemExit(f"Unknown RUN_MODE={settings.run_mode!r}. Use 'web' or 'cli'.")

if __name__ == "__main__":
    main()
