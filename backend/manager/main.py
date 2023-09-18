from manager import app
from manager.controllers.operators import operators_public_router, operators_private_router

background_tasks = set()



app.include_router(operators_public_router)
app.include_router(operators_private_router)
