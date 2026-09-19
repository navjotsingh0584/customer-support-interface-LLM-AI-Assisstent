from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends
from pathlib import Path
import uuid

from app.auth.dependencies import get_current_user
from app.services.vision_service import VisionService


router = APIRouter()

vision = VisionService()

UPLOAD_DIR = Path("app/uploads")

UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/analyze-image")
async def analyze_image(

    file: UploadFile = File(...),

    user: str = Depends(get_current_user)

):

    filename = (
        str(uuid.uuid4())
        +
        Path(file.filename).suffix
    )

    path = UPLOAD_DIR / filename

    contents = await file.read()

    with open(path, "wb") as f:
        f.write(contents)

    result = vision.analyze_image(
        str(path)
    )

    return {

        "filename": file.filename,

        "analysis": result

    }