from utils.routes import Routes
from .connector.routers import router as hik_router

__routes__ = Routes(
    routers=(
        hik_router,
    )
)

__ws_routes__ = Routes(
    routers=()
)
