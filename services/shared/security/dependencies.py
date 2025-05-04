from shared.security.dependencies import get_current_user

@app.get("/protected")
def protected_route(current_user = Depends(get_current_user)):
    return {"email": current_user["sub"]}
