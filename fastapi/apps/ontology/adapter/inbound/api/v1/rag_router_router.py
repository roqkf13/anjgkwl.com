from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException

from ontology.adapter.inbound.api.schemas.rag_router_schema import RouteQueryResponseSchema, RouteQuerySchema
from ontology.app.dtos.rag_router_dto import RouteQueryCommand
from ontology.app.ports.input.rag_router_use_case import RagRouterUseCase
from ontology.dependencies.rag_router_provider import get_rag_router_use_case

rag_router_query_router = APIRouter(tags=["route"])


@rag_router_query_router.post("/query", response_model=RouteQueryResponseSchema)
async def route_query(
    schema: Annotated[RouteQuerySchema, Body()],
    use_case: RagRouterUseCase = Depends(get_rag_router_use_case),
) -> RouteQueryResponseSchema:
    try:
        result = await use_case.route(RouteQueryCommand(text=schema.text))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e)) from e
    return RouteQueryResponseSchema(route=result.route, answer=result.answer, confidence=result.confidence)
