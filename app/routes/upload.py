from pathlib import Path
import uuid
import json

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    Form
)

from app.auth.dependencies import get_current_user
from app.services.session_store import SessionStore

from app.main import rag_service
from app.services.file_processor import FileProcessor
from app.services.pdf_processor import PDFProcessor
from app.services.image_router import ImageRouter


router = APIRouter()


UPLOAD_DIR = Path("app/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


file_processor = FileProcessor()
pdf_processor = PDFProcessor()
image_router = ImageRouter()
session_store = SessionStore()



# =========================
# UPLOAD ENDPOINT
# =========================

@router.post("/upload")
async def upload(

    session_id: str = Form(...),

    file: UploadFile = File(...),

    user: str = Depends(get_current_user)

):


    # =========================
    # SAVE FILE LOCALLY
    # =========================


    stored_filename = (
        str(uuid.uuid4())
        +
        Path(file.filename).suffix
    )


    path = UPLOAD_DIR / stored_filename


    contents = await file.read()


    with open(path, "wb") as f:

        f.write(contents)



    ext = Path(file.filename).suffix.lower()



    # =========================
    # PDF PROCESSING
    # =========================

    if ext == ".pdf":


        extracted = pdf_processor.process(
            str(path)
        )


        rag_service.add_text(

            text=extracted,

            source=file.filename,

            doc_type="pdf",

            metadata={

                "session_id": session_id,

                "filename": file.filename

            }

        )



        session_store.save_uploaded_file(

            session_id=session_id,

            filename=file.filename,

            stored_filename=stored_filename,

            file_type="pdf",

            content=extracted

        )



        return {


            "status": "processed",

            "type": "pdf",

            "session_id": session_id,

            "knowledge_added": True

        }




    # =========================
    # IMAGE PROCESSING
    # =========================

    elif ext in [

        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".tiff",
        ".webp",
        ".avif",
        ".heic"

    ]:


        result = image_router.process(
            str(path)
        )


        print(
            "\n========== VISION RESULT =========="
        )

        print(result)

        print(
            "===================================\n"
        )



        rag_service.add_text(

            text=f"""

SOURCE: IMAGE


TYPE:

{result['type']}


METHOD:

{result.get('source','vision')}



CONTENT:


{result.get(
    'analysis',
    'No vision analysis available'
)}

""",

            source=file.filename,

            doc_type="image",

            metadata={

                "session_id": session_id,

                "filename": file.filename

            }

        )



        vision_content = json.dumps({

            "type": result["type"],

            "analysis": result.get(

                "analysis",

                "No analysis available"

            ),

            "source": result.get(

                "source",

                "vision"

            )

        })



        session_store.save_uploaded_file(

            session_id=session_id,

            filename=file.filename,

            stored_filename=stored_filename,

            file_type="image",

            content=vision_content

        )



        return {


            "status": "processed",

            "type": result["type"],

            "method": result.get(

                "source",

                "vision"

            ),

            "session_id": session_id,

            "knowledge_added": True,

            "url": f"/uploads/{stored_filename}"

        }




    # =========================
    # TABLE PROCESSING
    # =========================


    elif ext in [

        ".csv",

        ".xlsx"

    ]:


        extracted = file_processor.process_table(
            str(path)
        )


        rag_service.add_text(

            text=extracted,

            source=file.filename,

            doc_type="table",

            metadata={

                "session_id": session_id,

                "filename": file.filename

            }

        )



        session_store.save_uploaded_file(

            session_id=session_id,

            filename=file.filename,

            stored_filename=stored_filename,

            file_type="table",

            content=extracted

        )



        return {


            "status": "processed",

            "type": "table",

            "session_id": session_id,

            "knowledge_added": True

        }



    # =========================
    # UNSUPPORTED
    # =========================


    return {


        "status": "error",

        "message": f"Unsupported file type: {ext}"

    }




# =========================
# GET UPLOADED FILES
# =========================


@router.get("/api/uploads/{session_id}")

def get_uploaded_files(

    session_id: str,

    user: str = Depends(get_current_user)

):


    files = session_store.get_uploaded_files(
        session_id
    )


    response = []



    for f in files:


        response.append({

            "filename": f["filename"],

            "stored_filename": f.get(
                "stored_filename"
            ),

            "file_type": f["file_type"],

            "created_at": f["created_at"],

            "url": (

                f"/uploads/{f['stored_filename']}"

                if f.get("stored_filename")

                else None

            )

        })



    return response