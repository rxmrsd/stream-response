"""main.py"""
from typing import Generator, Optional

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_google_vertexai import ChatVertexAI

DEFAULT_MESSAGE = "What is baseball?"
MODEL = "gemini-1.5-flash-preview-0514"

app = FastAPI()
model = ChatVertexAI(model_name=MODEL, streaming=True)


@app.get("/")
def read_root() -> str:
    return "Hello"


@app.post("/run")
def run_feedback(message: Optional[str] = None) -> str:
    if message is None:
        message = DEFAULT_MESSAGE
    response = model.invoke(message)
    return response.content


@app.post("/run_stream")
def stream_response(message: Optional[str] = None) -> StreamingResponse:
    if message is None:
        message = DEFAULT_MESSAGE
    gene = model.stream(message)
    chunk = text_response(gene)

    return StreamingResponse(
        chunk,
        status_code=200,
        headers=None,
        media_type=None,
        background=None,
    )


def text_response(gene: Generator):
    for chunk in gene:
        yield chunk.content
        yield "\n\n--------------------------\n\n"
