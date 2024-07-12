from langchain_community.document_loaders import YoutubeLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_vertexai import VertexAI
from langchain.chains.summarize import load_summarize_chain
from vertexai.generative_models import GenerativeModel
from langchain.prompts import PromptTemplate
from tqdm import tqdm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



class GeminiProcessor:
    def __init__(self, model_name, project) -> None:
        self.model = VertexAI(model_name=model_name,project=project)

    def generate_document_summary(self, document:list, **args):
        chain_type = "map_reduce" if len(document) > 10 else "stuff"

        chain = load_summarize_chain(
            
            llm=self.model,
            chain_type=chain_type,
            **args
        )
        return chain.invoke(document)
    
    def count_total_tokens(self,docs:list):
        temp_model = GenerativeModel("gemini-1.0-pro")
        total = 0
        logger.info("Counting number of token being used ....")
        for doc in tqdm(docs):
            total+=temp_model.count_tokens(doc.page_content).total_tokens



    def get_model(self):
        return self.model
    


class YoutubeProcessor:
    def __init__(self, genai_processor:GeminiProcessor) -> None:
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=0
        )
        self.gemini_processor = genai_processor

    def retrieve_youtube_document(self, video_url: str, verbose: bool = False):
        loader = YoutubeLoader.from_youtube_url(
            str(video_url), add_video_info=True)
        docs = loader.load()
        results = self.text_splitter.split_documents(docs)
        if verbose:
            author = results[0].metadata['author']
            length = results[0].metadata['length']
            title = results[0].metadata['title']
            total_size = len(results)
            logout = {"author": {author}, "length": {length},
                      "title": {title}, "total_size": {total_size}}
            logger.info(str(logout))
        return results
    
    def find_key_concepts(self,documents:list,group_size:int = 2):
        if group_size > len(documents):
            raise ValueError("Group size is larger than the number of documents")
        
        # find the number of documents in each group
        new_group_per_group = len(documents) // group_size+(len(documents)% group_size >0)

        # SPlit the documents in chunks of size num_docs_per_group
        groups = [documents[i:i+new_group_per_group] for i in range(0,len(documents),new_group_per_group)]

        batch_concepts = []

        logger.info("Finding Key concepts..")
        for group in tqdm(groups):
            # Combine contents of documents per group
            group_content = ""

            for doc in group:
                group_content += doc.page_content
            
            # prompt for findding concepts
            prompt = PromptTemplate(template="""
                     Find the key concepts and their definitions from the following text:
                     {text}.
                     Respond only in clean JSON format without any labels or additional text. The output exactly should look like this:
                     {{"concept1": "definition1", "concept2": "definition2"}}
                     """, input_variables=["text"])
            
            # Create chain
            chain = prompt | self.gemini_processor.model

            concept = chain.invoke({"text":group_content})
            # append all the concepts to the batch concepts list to concant together to display 
            batch_concepts.append(concept)

        return batch_concepts
