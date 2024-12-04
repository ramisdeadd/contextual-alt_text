from typing import Annotated
import uvicorn
from database import create_db_and_tables, get_session, SessionDep
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
    await create_db_and_tables()
    # async for session in get_session():
    #    await create_admin_user(session)
    yield
    print("Stopping Server ....")

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix='/auth')
app.include_router(post_router, prefix="/post")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, session: SessionDep, token: Annotated[str, Cookie(...)] = None):
    try:
        user = await get_current_user(token=token, allow=True, session=session)
        if user == None:
            return templates.TemplateResponse("pages/index.html", {"request": request, "user": None, "nlp": nlp_models_dict, "cv": vision_models_dict})
        first_name_display = user.first_name.title()
        return templates.TemplateResponse("pages/index.html", {"request": request, "user": user, "first_name_display": first_name_display, "nlp": nlp_models_dict, "cv": vision_models_dict})
    except HTTPException as error: 
        if error.status_code == status.HTTP_401_UNAUTHORIZED:
            response = RedirectResponse(url="auth/login", status_code=status.HTTP_302_FOUND)
            response.delete_cookie("token")
            return response
        raise error
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


