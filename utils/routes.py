from collections.abc import Iterable
from dataclasses import dataclass

from aiogram import Dispatcher
from fastapi import APIRouter
from fastapi import FastAPI

from config.settings import APP_SETTINGS


@dataclass(frozen=True)
class Routes:
    routers: Iterable[APIRouter]

    def register_routes(self, app: FastAPI, prefix=APP_SETTINGS.API_V1_PREFIX):
        for router in self.routers:
            app.include_router(router, prefix=prefix)


@dataclass(frozen=True)
class Handlers:
    handlers: Iterable

    def register_handlers(self, dp: Dispatcher):
        for router in self.handlers:
            dp.include_router(router)
