from manager import app
from manager.controllers.charge_points import charge_points_router
from manager.controllers.operators import operators_public_router, operators_private_router


app.include_router(operators_public_router)
app.include_router(operators_private_router)
app.include_router(charge_points_router)
