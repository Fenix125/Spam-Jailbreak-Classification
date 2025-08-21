from app.backend.config import settings

def main():
    if settings.run_mode == "web":
        import uvicorn
        uvicorn.run(
            "app.backend.web_app:app",
            host="0.0.0.0",
            port=8000
        )
    elif settings.run_mode == "cli":
        from app.backend.terminal_app import cli
        cli()
    else:
        raise SystemExit(f"Unknown RUN_MODE={settings.run_mode!r}. Use 'web' or 'cli'.")

if __name__ == "__main__":
    main()
