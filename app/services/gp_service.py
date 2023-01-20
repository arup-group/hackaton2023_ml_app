import pickle
from fastapi.responses import JSONResponse
import numpy as np
import os
from pydantic import BaseModel, Field
from fastapi import HTTPException
from app.enums import AvailableModelsEnum

class InputParam(BaseModel):
    load : float = Field(..., ge=2, le=10)
    span_x : float = Field(..., ge=5, le=12)
    span_y : float = Field(..., ge=5, le=12)
    thickness: float = Field(..., get=0.1, let=0.4)

GP_MODELS_PATH = f"{os.getcwd()}\\app\\gp_trained\\"


def run_gp(
    gp_model: AvailableModelsEnum,
    load : float, 
    span_x: float, 
    span_y: float, 
    thickness: float
):  

    with open(f"{GP_MODELS_PATH}//{gp_model.value}", "rb") as file:
        gp = pickle.load(file)
        scale_mean_X = pickle.load(file)
        scale_var_X = pickle.load(file)
        scale_mean_Y = pickle.load(file)
        scale_var_Y = pickle.load(file)
    
    # Validation Inputs
    try:
        InputParam(load=load, span_x=span_x, span_y=span_y, thickness=thickness)
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e),
        )
    load_scaled = (load - scale_mean_X[0])/scale_var_X[0] 
    span_x_scaled = (span_x - scale_mean_X[1])/scale_var_X[1] 
    span_y_scaled = (span_y - scale_mean_X[2])/scale_var_X[2] 
    thickness_scaled = (thickness - scale_mean_X[3])/scale_var_X[3] 
    
    y_scaled, std_scaled = gp.predict([[load_scaled, span_x_scaled, span_y_scaled, thickness_scaled ]], return_std = True)
    
    y = scale_var_Y[0]*y_scaled[0]+scale_mean_Y[0]
    std = scale_var_Y[0]*std_scaled[0]
    
    return JSONResponse(
        content={
        'Response Factor - mean' : np.round(y,3),
        'Response Factor - std' : np.round(std,3),
        'Response Factor - CI-68%': list(np.round([max(y-std, 0), y+std],3)),
        'Response Factor - CI-95%': list(np.round([max(y-2*std, 0), y+2*std],3)),
        'Response Factor - CI-99.7%': list(np.round([max(y-3*std, 0), y+3*std],3)),
        'Response Factor - CV [%]': np.round((std/y)*100,3)
        },
        status_code=200
    )