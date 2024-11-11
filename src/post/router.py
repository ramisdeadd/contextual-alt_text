from pathlib import Path
from typing import Annotated
from fastapi import File, Form, UploadFile, status, Cookie, APIRouter
from fastapi.responses import JSONResponse, RedirectResponse
from post.dependencies import (
    vision_models_dict, 
    nlp_models_dict,
    generate_image_hash,
    save_alt_gen,
    save_image_gen,
    check_image_exist,
);
from generate import create_alttext
from auth.dependencies import get_current_user
import PIL.Image

router = APIRouter()

@router.post("/")
async def generate_alt_text(
    text: Annotated[str, Form()], 
    nlp: Annotated[str, Form()],
    cv: Annotated[str, Form()],
    token: Annotated[str, Cookie(...)] = None,
    img: UploadFile = File(...)
):
    size = (1920, 1080)

    vision_model = vision_models_dict[cv]
    nlp_model = nlp_models_dict[nlp]

    user = await get_current_user(token=token, allow=True)
    if user == None:
        response = RedirectResponse("/auth/login", status_code=status.HTTP_302_FOUND)
        return response
    
    img_content = await img.read()
    img_path = Path(f"images/{img.filename}")
    with open(img_path, "wb") as f:
        f.write(img_content)

    with PIL.Image.open(img_path) as image:
        image.save(img_path, dpi=size)
        image_hash = await generate_image_hash(img_path)

    image_exist = await check_image_exist(user, image_hash)  
    generator_output = create_alttext(text, img_path, image_exist, vision_model=vision_model, nlp_model=nlp_model)
    image_db = await save_image_gen(user, image_hash, generator_output["image-caption"], vision_model)
    alttext_db = await save_alt_gen(image_db, generator_output["alt-text"], nlp_model)

    # Remove image after use
    img_path.unlink()

    return JSONResponse(content={
        "generated-alt-text": generator_output["alt-text"],
        "generated-image-caption": generator_output["image-caption"],
    }) 
