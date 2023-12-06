from pydantic import BaseModel
from typing import Optional, List
import json
import numpy as np

class FIMultiEntradaSchema(BaseModel):

    resgate: str = "1"
    capta: str = "2"
    patliq: str = "1000000"
    pattotal: str = "3"

class FIMultiSaidaSchema(BaseModel):

    sugest_str: str