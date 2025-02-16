"""Please install dependencies using:
pip install openai moviepy ffmpeg
"""
import json
import os
from typing import Generator

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.moviepy_video import MoviePyVideoTools
# from agno.tools.openai import OpenAITools
# from google import genai
from faster_whisper import WhisperModel, transcribe
import torch
from transformers import pipeline
from transformers.utils import is_flash_attn_2_available
import weave

weave.init('multi-modal-hackathon')

@weave.op()
def transcribe_audio(filename: str):
    pipe = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-large-v3", # select checkpoint from https://huggingface.co/openai/whisper-large-v3#model-details
            torch_dtype=torch.float16,
            device="cuda:0", # or mps for Mac devices
            model_kwargs={"attn_implementation": "flash_attention_2"} if is_flash_attn_2_available() else {"attn_implementation": "sdpa"},
            )

    outputs = pipe(
        filename,
        chunk_length_s=30,
        batch_size=24,
        return_timestamps=True,
    )
    return outputs

video_tools = MoviePyVideoTools(
    process_video=True, generate_captions=True, embed_captions=True
)

@weave.op()
def extract_chunks() -> list[str]:
    return json.load(open("chunks.json"))['chunks']

@weave.op()
def write_chunks(chunks: str) -> None:
    with open("chunks.txt", "w") as f:
        f.write(chunks)

opinion_agent = Agent(
    name="Video Caption Generator Agent",
    model=Gemini(
        id="gemini-2.0-flash-exp",
        api_key=os.getenv("GEMINI_API_KEY"),
    ),
    tools=[extract_chunks, write_chunks],
    description="You are an AI agent that can evaluate how truthy a statement is.",
    instructions=[
        "Process the chunks to generate truthiness scores.",
        "1. Extract chunks from the json using the extract_chunks tool",
        "2. Cast an opinion for each chunk",
        "3. Call write_chunks to write the opinions to a file",
    ],
    markdown=True,
)


opinion_agent.print_response(
    "For each chunk returned from extract_chunks, give a score between 0 and 1 based on how true the content is and write using write_chunks"
)
