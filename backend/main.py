from app import app
from controllers.charge_points import charge_points_router
from controllers.drivers import drivers_router
from controllers.operators import operators_public_router, operators_private_router

app.include_router(drivers_router)
app.include_router(operators_public_router)
app.include_router(operators_private_router)
app.include_router(charge_points_router)
