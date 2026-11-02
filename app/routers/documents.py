from fastapi import APIRouter, Depends, status

from app.deps import StoreDep
from app.schemas import DocumentIn, DocumentOut
from app.security import require_api_key

router = APIRouter(prefix="/documents", tags=["documents"], dependencies=[Depends(require_api_key)])


@router.post("", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
async def add_document(body: DocumentIn, store: StoreDep) -> DocumentOut:
    doc = store.add(title=body.title, content=body.content)
    return DocumentOut(id=doc.id, title=doc.title, chars=len(doc.content))
