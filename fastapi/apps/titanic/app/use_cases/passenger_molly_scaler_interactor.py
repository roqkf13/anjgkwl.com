import logging

from titanic.adapter.inbound.api.schemas.passenger_molly_scaler_schema import MollyScalerSchema
from titanic.app.dtos.passenger_molly_scaler_dto import MollyScalerQuery, MollyScalerResponse
from titanic.app.ports.input.passenger_molly_scaler_use_case import MollyScalerUseCase
from titanic.app.ports.output.passenger_molly_scaler_port import MollyScalerPort

logger = logging.getLogger(__name__)


class MollyScalerInteractor(MollyScalerUseCase):

    def __init__(self, repository: MollyScalerPort):
        self.repository = repository

    async def introduce_myself(self, schema: MollyScalerSchema) -> MollyScalerResponse:
        return await self.repository.introduce_myself(MollyScalerQuery(
            id=schema.id,
            name=schema.name,
        ))

    async def scale_features(self, schema: MollyScalerSchema) -> MollyScalerResponse:
        raise NotImplementedError



#테스트용 의미없는주석