from datetime import datetime
from typing import Union

from  model import Base

# colunas = 'RESG_DIA', 'CAPTC_DIA', 'VL_PATRIM_LIQ', 'VL_TOTAL', 'SUGESTÃO'

class FIMulti(Base):

    RESG_DIA: float = 1
    CAPTC_DIA: float = 2
    VL_PATRIM_LIQ: float = 1000000
    VL_TOTAL: float = 3 