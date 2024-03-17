import os
import PyPDF2
import re
import pysqlite3
import sys
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
from chromadb import Client, Settings
from chromadb.utils import embedding_functions
from PyPDF2 import PdfReader
from typing import List, Dict, Annotated
import requests
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import uvicorn
from utils.utils import verify_pdf_path, get_text_chunks, load_pdf, query


ef = embedding_functions.ONNXMiniLM_L6_V2()
messages = []

# collection = CreateClient.create_collection()
client = Client(settings = Settings(persist_directory="./", is_persistent=True))
collection_ = client.get_or_create_collection(name="test", embedding_function=ef)
def clear_coll():
    client.delete_collection(collection_.name)
    print("Collection deleted successfully")
 

def add_text_to_collection(file: str, word: int = 200) -> None:
    docs = load_pdf(file, word)
    docs_strings = []
    ids = []
    metadatas = []
    id = 0
    for page_no in docs.keys():      
        for doc in docs[page_no]:
            docs_strings.append(doc)
            metadatas.append({'page_no':page_no})
            ids.append(id)
            id+=1

    collection_.add(
        ids = [str(id) for id in ids],
        documents = docs_strings,
        metadatas = metadatas,
    )
    return "PDF embeddings successfully added to collection"

def query_collection(texts: str, n: int) -> List[str]:
    result = collection_.query(
                  query_texts = texts,
                  n_results = n,
                 )
    documents = result["documents"][0]
    metadatas = result["metadatas"][0]
    resulting_strings = []
    for page_no, text_list in zip(metadatas, documents):
        resulting_strings.append(f"Page {page_no['page_no']}: {text_list}")
    return resulting_strings

def get_response(queried_texts: List[str],) -> List[Dict]:
    global messages
    
    messages = [
                {"role": "system", "content": "You are a helpful assistant. <s>[INST]Keep in mind that you will start the answer with the keyword 'Your Answer' and should end the answer with 'End of your answer'. Your answer will try to answer with information provided reference.[/INST]<s>[INST] Use the string annotated as 'Reference' and appears before 'ques'[/INST] <s>[INST] And will always answer the question asked in 'ques:' and \
                  you will answer the 'ques' using 'Reference' ellaboratively and elegantly combining information from all the pages no.[/INST]."},
                {"role": "user", "content": ''.join(queried_texts)}
                ]
    message = ' '.join([str(elem) for elem in messages])
    response = query({"inputs": message,})
    messages = messages + [{"role":'assistant', 'content': response}]
    return response

def get_answer(query: str, n: int):
    queried_texts = query_collection(texts = query, n = n)
    queried_string = [''.join(text) for text in queried_texts]
    queried_string = f"Reference:{queried_string[0]}" + f"ques: {query}"
    answer = get_response(queried_texts = queried_string,)
    message = ' '.join([str(elem) for elem in answer])
    pattern = r'Your Answer: (.+?)End of your answer\.'
    match = re.search(pattern, message)
    if match:
        substring_after_assistant = match.group(1)
        substring_after_assistant = substring_after_assistant.replace('\\n', '\n')
        return substring_after_assistant
    else:
        return message

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/query/{pdf_path:path}") 
def handle_query(pdf_path: str, request: QueryRequest):
  query = request.query
  verify_pdf_path(pdf_path)
  add_text_to_collection(pdf_path)
  try:
    answer = get_answer(query, 5)  
    return {"answer": answer}
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)