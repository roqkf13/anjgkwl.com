from fastapi import Depends

from ontology.adapter.outbound.rag_router.rag_router_classifier_adapter import get_rag_router_classifier
from ontology.app.ports.input.rag_router_use_case import RagRouterUseCase
from ontology.app.ports.output.rag_router_classifier_port import RagRouterClassifierPort
from ontology.app.use_cases.rag_router_interactor import RagRouterInteractor
from rag.app.ports.input.rag_document_use_case import RagDocumentUseCase
from rag.dependencies.rag_document_provider import get_rag_document_use_case


def get_rag_router_use_case(
    classifier: RagRouterClassifierPort = Depends(get_rag_router_classifier),
    rag_use_case: RagDocumentUseCase = Depends(get_rag_document_use_case),
) -> RagRouterUseCase:
    return RagRouterInteractor(classifier=classifier, rag_use_case=rag_use_case)
