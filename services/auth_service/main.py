from auth_service.app.main import app


@app.get("/health", tags=["health"])
def root_health():
    return {"status": "ok"}
