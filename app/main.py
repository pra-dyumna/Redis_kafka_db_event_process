from fastapi import FastAPI
from datetime import datetime
from app.redis_client import get_redis
from app.schema import DocumentRequest
from app.config import STREAM_NAME

app = FastAPI()
r = get_redis()

@app.post("/upload")
def upload_document(data: DocumentRequest):
    event = {
        "event_type": "document_uploaded",
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": data.user_id,
        "doc_url": data.doc_url,
        "company_url": data.company_url,
        "status": "pending"
    }

    message_id = r.xadd(STREAM_NAME, event)

    return {
        "status": "queued",
        "message_id": message_id
    }