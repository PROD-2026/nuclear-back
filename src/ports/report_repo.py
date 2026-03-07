from abc import ABC

from src.domain.entities.report import Report
from src.ports.repo import IRepository


class IReportRepository(IRepository[Report], ABC): ...
