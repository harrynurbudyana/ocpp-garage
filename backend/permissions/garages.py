from fastapi import Request

from exceptions import Forbidden
from permissions import BasePermission


class CanOperatorManageGarages(BasePermission):

    async def has_permissions(self, request: Request):
        if not request.state.operator.is_superuser:
            raise Forbidden
