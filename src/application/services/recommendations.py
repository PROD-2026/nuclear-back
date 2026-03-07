from src.ports.ml import IMLProvider


class RecommendationsService:
    def __init__(self, ml_provider: IMLProvider) -> None:
        self._ml = ml_provider

    async def get_recommendations(self, vulnerabilities: list[str]) -> str:
        return await self._ml.get_recommendations(vulnerabilities)
