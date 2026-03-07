from litestar import Router

from src.api.routers.health import HealthController
from src.api.routers.reports import ReportController

routers = Router(path="/", route_handlers=[HealthController, ReportController])
