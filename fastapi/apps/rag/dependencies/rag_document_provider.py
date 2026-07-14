from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from rag.adapter.outbound.repositories.rag_document_repository import RagDocumentRepository
from rag.app.ports.input.rag_document_use_case import RagDocumentUseCase
from rag.app.ports.output.rag_document_port import RagDocumentPort
from rag.app.use_cases.rag_document_interactor import RagDocumentInteractor


def get_rag_document_repository(db: AsyncSession = Depends(get_db)) -> RagDocumentPort:
    return RagDocumentRepository(session=db)


def get_rag_document_use_case(
    repository: RagDocumentPort = Depends(get_rag_document_repository),
) -> RagDocumentUseCase:
    return RagDocumentInteractor(repository=repository)
