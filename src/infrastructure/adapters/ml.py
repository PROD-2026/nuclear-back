import httpx

from src.domain.vaule_objects.vulnerability import VulnerabilityMLInfo
from src.ports.ml import IMLProvider


class MLProvider(IMLProvider):
    def __init__(self, base_url: str) -> None:
        self._client = httpx.AsyncClient(base_url=base_url, timeout=30)

    async def check_vulnerabilities(
        self, values: list[str]
    ) -> list[VulnerabilityMLInfo]:
        resp = await self._client.post("/predict_batch", json={"texts": values})
        resp.raise_for_status()

        data = resp.json()

        return [
            VulnerabilityMLInfo(
                text=info["text"],
                is_vulnerability=bool(info["class"]),
                probability=info["probability"],
                severity=info["severity"].lower(),
            )
            for info in data["predictions"]
        ]

    async def get_recommendations(self, vulnerabilities: list[str]) -> str:
        resp = await self._client.post(
            "/recommend", json={"text": " ".join(vulnerabilities)}
        )
        resp.raise_for_status()

        data = resp.json()

        return data["text"]
