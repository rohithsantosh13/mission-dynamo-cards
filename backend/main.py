from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from fastapi.middleware.cors import CORSMiddleware


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
    from langchain_community.document_loaders import YoutubeLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    #
    loader = YoutubeLoader.from_youtube_url(
        str(request.youtube_link), add_video_info=True)
    docs = loader.load()
    print(f"{type(docs)}")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=0)
    results = text_splitter.split_documents(docs)

    print(f"{type(results)}")

    author = results[0].metadata['author']
    length = results[0].metadata['length']
    title = results[0].metadata['title']

    total_size = len(results)
    return {

        "author": author,
        "length": length,
        "title": title,
        "total_size": total_size
    }


@app.get("/health")
def health():
    print("Health is called from the FASTAPI calls uhuuu")
    return {"status": "ok"}
