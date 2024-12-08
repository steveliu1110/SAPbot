from langchain_community.document_loaders import FireCrawlLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.utils import filter_complex_metadata
import json
from dotenv import load_dotenv
import os
from datetime import datetime

# custom functions
from .vstore import updateChroma, getVectorStore
from .sqlstore import update_scrapy_data

from ..models import Website
load_dotenv()

# update the scrapy data for multiple websites
def update_scrapy(url, chunk_size = 1024, chunk_overlap = 100):
    try:
        print('```````````````````````````````')
        loader = FireCrawlLoader(  
            api_key=os.getenv('FIRECRAWL_API_KEY'),  # Make sure the API key is set in .env  
            url=url,  
            mode="crawl",  
            params={
                "limit":20, 
                "maxDepth": 2,
                "scrapeOptions": {
                    "onlyMainContent": True,
                    "formats" : ["html", "markdown"],
                    "waitFor": 1000,  # wait for a second for pages to load
                    "timeout": 10000,  # timeout after 10 seconds
                }
            },
        )
        docs = loader.load()
        if not docs:  
            raise ValueError("No documents were loaded. Please check the URL and the FireCrawl API key.")  
        text_splitter = RecursiveCharacterTextSplitter(  
            chunk_size=chunk_size,   
            chunk_overlap=chunk_overlap
        )
        docs = filter_complex_metadata(docs)
        splits = text_splitter.split_documents(docs)
        ids = [f'{url[8:]}_{i}' for i in range(len(splits))]
        #update chroma
        try:
            updateChroma(docs, ids)
            late_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            chunk_count = len(splits)
            return (url, late_update, chunk_count)
        except Exception as ee:
            print("update chroma error", ee)
            return False
        return ()

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return False