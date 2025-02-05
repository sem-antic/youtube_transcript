import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi

app = FastAPI()


class GetTranscriptBody(BaseModel):
    video_id: str
    languages: list[str] = ['ru']


@app.post("/api/v1/get_transcript")
def predict_customer_intents(body: GetTranscriptBody):
    result = YouTubeTranscriptApi.get_transcript(body.video_id, languages=['ru'])
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
