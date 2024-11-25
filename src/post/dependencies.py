import hashlib
from pathlib import Path
from sqlmodel import Session, select
from post.models import AltTextEdit
from post.schemas import AltText, Image
from auth.schemas import User
from database import engine, SessionDep

vision_models_dict = {"CLIPCAP": "CLIPCAP", "BLIP": "BLIP", "GPT2": "GPT2", "BLIP2": "BLIP2"}
nlp_models_dict =  {"BART": "BART", "PEGASUS": "PEGASUS", "T5": "T5", "FlanT5": "FlanT5"}

async def save_alt_gen(
        image: Image,
        alt: str,
        alt_gen: str,
        session: SessionDep,
):
    alt_text = AltText(
        image_id = image.id,
        alt = alt,
        alt_gen = alt_gen
    )

    session.add(alt_text)
    await session.commit()
    await session.refresh(alt_text)
    
    return alt_text

async def check_image_exist(
        user: User,
        image_hash: str,
        session: SessionDep,
):
    # Check if image hash already exists
    statement = select(Image).where(
        Image.hash == image_hash,
        Image.user_id == user.id
    )
    results = await session.execute(statement)
    image = results.first()

    # Returns already existing image
    if image is not None: 
        return image
    else:
        return None

async def save_image_gen(
        user: User,
        image_hash: str,
        caption: str,
        caption_gen: str,
        session: SessionDep,
):
    image = Image(
        caption = caption,
        caption_gen = caption_gen,
        hash = image_hash,
        user_id = user.id
    )

    session.add(image)
    await session.commit()
    await session.refresh(image)

    return image
    
def generate_image_hash(
        img_path: Path
):
        with open(img_path, "rb") as f:
            bytes = f.read()
            readable_hash = hashlib.md5(bytes).hexdigest()

        return readable_hash

def rename_file_with_hash(original_path: Path, hash_value: str) -> Path:
    new_path = original_path.with_name(f"{hash_value}{original_path.suffix}")
    original_path.rename(new_path)
    return new_path

async def save_alt_user(
        user: User,
        alt_edit: str,
        session: SessionDep,
):
    user_query = select(User).where(User.id == user.id)
    user_result = await session.excute(user_query)
    user = user_result.first()

    image_query = await select(Image).where(Image.user_id == user.id).order_by(Image.id.desc())
    image_result = session.excute(image_query)
    image = image_result.first()

    if image:
        # Get the most recent alt-text for the image
        alt_text_query = select(AltText).where(AltText.image_id == image.id).order_by(AltText.id.desc())
        alt_text_result = await session.excute(alt_text_query)
        db_alt = alt_text_result.first()

        if db_alt:
            # Update the alt-text
            db_alt.alt_edit = alt_edit
            session.add(db_alt)
            await session.commit()
            await session.refresh(db_alt)
            return db_alt
        
    return None