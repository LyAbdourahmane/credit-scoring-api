# ---------- Schéma d'entrée ----------
from pydantic import BaseModel, Field, field_validator

class CreditInput(BaseModel):
    AMT_REQ_CREDIT_BUREAU_YEAR: float = Field(..., ge=0)
    HOUR_APPR_PROCESS_START: int = Field(..., ge=0, le=23)
    AMT_ANNUITY: float = Field(..., gt=0)
    AMT_CREDIT: float = Field(..., gt=0)
    EXT_SOURCE_3: float = Field(None, ge=0, le=1)
    EXT_SOURCE_2: float = Field(None, ge=0, le=1)
    CODE_GENDER: str
    FLAG_PHONE: int = Field(..., ge=0, le=1)
    AMT_GOODS_PRICE: float = Field(..., gt=0)
    FLAG_OWN_CAR: str
    NAME_FAMILY_STATUS: str

    @field_validator("CODE_GENDER")
    def validate_gender(cls, v):
        if v not in ["M", "F"]:
            raise ValueError("CODE_GENDER must be 'M' or 'F'")
        return v

    @field_validator("FLAG_OWN_CAR")
    def validate_car(cls, v):
        if v not in ["Y", "N"]:
            raise ValueError("FLAG_OWN_CAR must be 'Y' or 'N'")
        return v