from fastapi import APIRouter
from app.services import gp_service
from app.enums import AvailableModelsEnum
router = APIRouter(prefix="/GP")

@router.get("/prediction", tags=["Gaussian Process"])
async def get_GP_prediction(
    gp_model: AvailableModelsEnum,
    load : float ,
    span_x: float, 
    span_y: float, 
    thickness: float
    ):
    """
        Limits on the input parameters:
            - load: [2, 10] kN/mq, 
            - span_x: [5,12] m, 
            - span_y: [5,12] m, 
            - thickness: [0.1, 0.4] m
    """
    return gp_service.run_gp(gp_model=gp_model,load=load, span_x=span_x, span_y=span_y, thickness=thickness)