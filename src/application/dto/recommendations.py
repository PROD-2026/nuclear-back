from litestar.dto import DataclassDTO, DTOConfig

from src.domain.vaule_objects.recommendations import Recommendations


class RecommendationsGetDTO(DataclassDTO[Recommendations]):
    config = DTOConfig()
