# generated by datamodel-codegen:
#   filename:  claim_hDAO.json

from __future__ import annotations

from pydantic import BaseModel, Extra


class ClaimHDAOParameter(BaseModel):
    class Config:
        extra = Extra.forbid

    hDAO_amount: str
    objkt_id: str
