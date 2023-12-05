from pydantic import BaseModel
from typing import Optional, List
from model.FIMulti import FIMulti
import json
import numpy as np

class FIMultiSchema(BaseModel):
    """ Define como um novo paciente a ser inserido deve ser representado
    """
    RESG_DIA: float = 1
    CAPTC_DIA: float = 2
    VL_PATRIM_LIQ: float = 1000000
    VL_TOTAL: float = 3