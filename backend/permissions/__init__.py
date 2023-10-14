from fastapi import Request


class BasePermission:

    async def __call__(self, request: Request):
        return await self.has_permissions(request)

    async def has_permissions(self, request: Request):
        return True
