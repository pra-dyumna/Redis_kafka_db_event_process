from pydantic import BaseModel

class DocumentRequest(BaseModel):
    user_id: int
    doc_url: str
    company_url: str