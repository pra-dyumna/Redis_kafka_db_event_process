from fastapi import FastAPI
from pydantic import BaseModel
import redis
import json

app = FastAPI()

# Redis connection
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Request model
class DocumentRequest(BaseModel):
    user_id: int
    doc_url: str
    company_url: str


# Upload API (Producer)
@app.post("/upload")
def upload_document(data: DocumentRequest):
    job = data.model_dump()
    
    # Push into Redis queue
    r.lpush("document_queue", json.dumps(job))
    
    return {
        "status": "queued",
        "message": "Data stored in Redis",
        "data": job
    }


# Get API (Consumer simulation)
@app.get("/get")
def get_document():
    job = r.rpop("document_queue")  # FIFO
    
    if not job:
        return {"message": "No data found in queue"}
    
    return {
        "status": "fetched",
        "data": json.loads(job)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)