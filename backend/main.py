
from fastapi import FastAPI
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware
from services.genai import YoutubeProcessor, GeminiProcessor

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
genai_processor = GeminiProcessor(
    model_name='gemini-pro',
    project="radicalaisamplegemini",
    location='us-east4'
)


class VideoAnalysisRequest(BaseModel):
    youtube_link: str


@app.post("/analyze_video/")
def analyze_video(request: VideoAnalysisRequest):

    processor = YoutubeProcessor(genai_processor)

    result = processor.retrieve_youtube_documents(str(request.youtube_link))

    # summary = genai_processor.generate_document_summary(result, verbose = True)
    sample_size = 10
    key_concepts = processor.find_key_concepts(
        result, verbose=True)
    return {
        "key_concepts": key_concepts
    }
