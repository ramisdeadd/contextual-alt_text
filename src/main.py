from typing import Annotated
import uvicorn
from database import create_db_and_tables
from auth.utilities import create_admin_user
from auth.dependencies import get_current_user
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, status, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from auth.router import router as auth_router
from post.router import router as post_router
from configs import templates
from post.dependencies import nlp_models_dict, vision_models_dict

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Server ....")
    create_db_and_tables()
    create_admin_user()
    yield
    print("Stopping Server ....")

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix='/auth')
app.include_router(post_router, prefix="/posts")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, token: Annotated[str, Cookie(...)] = None):
    try:
        user = await get_current_user(token=token, allow=True)
        if user == None:
            return templates.TemplateResponse("/pages/index.html", {"request": request, "user": None, "nlp": nlp_models_dict, "cv": vision_models_dict})
        return templates.TemplateResponse("/pages/index.html", {"request": request, "user": user, "nlp": nlp_models_dict, "cv": vision_models_dict})
    except HTTPException as error: 
        if error.status_code == status.HTTP_401_UNAUTHORIZED:
            response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
            response.delete_cookie("token")
            return response
        raise error
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


