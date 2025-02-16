"""Please install dependencies using:
pip install openai moviepy
"""
import os

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.moviepy_video import MoviePyVideoTools
import torch
from transformers import pipeline
from transformers.utils import is_flash_attn_2_available
import weave

# from faster_whisper import WhisperModel, transcribe

weave.init('multi-modal-hackathon')

# whisper_model = WhisperModel('turbo')


video_tools = MoviePyVideoTools(
    process_video=True, generate_captions=True, embed_captions=True
)

# @weave.op()
# def generate_transcript(mp3_filename: str) -> list[dict]:
    # segments, _info = whisper_model.transcribe(mp3_filename)
    # return [{ "text": segment.text, "timestamps": segment.timestamps } for segment in segments]

@weave.op()
def generate_transcript(mp3_filename: str) -> list[dict]:
    pipe = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-large-v3", # select checkpoint from https://huggingface.co/openai/whisper-large-v3#model-details
        torch_dtype=torch.float16,
        device="cuda:0", # or mps for Mac devices
        model_kwargs={"attn_implementation": "flash_attention_2"} if is_flash_attn_2_available() else {"attn_implementation": "sdpa"},
    )
    outputs = pipe(
        mp3_filename,
        # chunk_length_s=30,
        batch_size=24,
        return_timestamps=True,
    )
    print(outputs)
    return outputs


video_caption_agent = Agent(
    name="Video Caption Generator Agent",
    model=Gemini(
        id="gemini-2.0-flash-exp",
        api_key=os.getenv("GEMINI_API_KEY"),
    ),
    tools=[video_tools, generate_transcript],
    description="You are an AI agent that can generate and embed captions for videos.",
    instructions=[
        "When a user provides a video, process it to generate captions.",
        "Use the video processing tools in this sequence:",
        "1. Extract audio from the video using extract_audio",
        "2. Transcribe the audio using generate_transcript",
        "3. Generate SRT captions using create_srt",
        "4. Embed captions into the video using embed_captions",
    ],
    markdown=True,
)


video_caption_agent.print_response(
    "Generate captions for highlights.webm and embed them in the video"
)
