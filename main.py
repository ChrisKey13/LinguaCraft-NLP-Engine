from fastapi import FastAPI
from linguacraft.linguistic_processor.linguistic_processor import LinguisticProcessor

app = FastAPI()

linguistic_processor = LinguisticProcessor()

@app.post("/process/")
def process_text(text: str):
    return linguistic_processor.process_text(text)