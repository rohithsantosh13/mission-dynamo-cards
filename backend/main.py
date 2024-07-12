from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from fastapi.middleware.cors import CORSMiddleware
from services.genai import YoutubeProcessor, GeminiProcessor


class VideoAnalysisRequest(BaseModel):
    youtube_link: HttpUrl


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze_video")  # Change this line
def analyze_video(request: VideoAnalysisRequest):
   
    genai_processor = GeminiProcessor(model_name='gemini-pro',project="radicalaisamplegemini")
   
    yt = YoutubeProcessor(genai_processor=genai_processor)
    results = yt.retrieve_youtube_document(video_url=request.youtube_link, verbose=False)
    
    summary = genai_processor.generate_document_summary(results,verbose = True)

    # find the key concepts

    key_concepts = yt.find_key_concepts(results,group_size = 2)

    return {"key_concepts": key_concepts}


@app.get("/health")
def health():
    return {"status": "ok"}
