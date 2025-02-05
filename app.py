import io
import os

import googleapiclient.discovery
import uvicorn
from fastapi import FastAPI
from googleapiclient.http import MediaIoBaseDownload
from pydantic import BaseModel

from config import YOUTUBE_API_KEY

app = FastAPI()


class GetTranscriptBody(BaseModel):
    video_id: str
    language: str = 'ru'


def get_subtitles(video_id: str, lang: str = 'ru'):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=YOUTUBE_API_KEY)

    request = youtube.captions().download(id=video_id, tlang=lang)

    fname = f"files/{video_id}"
    fh = io.FileIO(fname, "wb")

    download = MediaIoBaseDownload(fh, request)
    complete = False
    while not complete:
        status, complete = download.next_chunk()

    with open(fname, 'r', encoding='utf-8') as f:
        data = f.read()

    os.remove(fname)
    return data


@app.post("/api/v1/get_transcript")
async def predict_customer_intents(body: GetTranscriptBody):
    data = get_subtitles(body.video_id)
    return data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
