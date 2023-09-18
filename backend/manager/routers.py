from fastapi import APIRouter

from manager.services.operators import AuthRoute


class AuthenticatedRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.route_class = AuthRoute


class AnonymousRouter(APIRouter):
    pass