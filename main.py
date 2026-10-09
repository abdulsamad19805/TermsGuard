from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
from typing import List
import pdfplumber
import ollama
import io

app = FastAPI(title="ToS & Contract Risk Analyzer")

class RiskItem(BaseModel):
    category: str = Field(description="e.g., Billing, Data Privacy, Legal Rights")
    severity: str = Field(description="HIGH, MEDIUM, or LOW")
    flag_title: str = Field(description="Short title for the issue")
    original_quote: str = Field(description="Exact snippet from contract text")
    plain_english: str = Field(description="Simple explanation of why this matters")

class ContractAnalysis(BaseModel):
    overall_risk_rating: str = Field(description="HIGH, MEDIUM, or LOW")
    executive_summary: str = Field(description="2-3 sentence overview")
    red_flags: List[RiskItem] = Field(default_factory=list)

class TextRequest(BaseModel):
    text: str


def analyze_chunk_with_ollama(text_chunk: str) -> ContractAnalysis:
    prompt = f"""
    You are a consumer protection lawyer. Analyze the following contract snippet for dangerous or anti-consumer terms:
    1. Automatic renewal, tricky cancellation, or hidden fees.
    2. Data selling, tracking, or sharing with 3rd parties.
    3. Waiving class-action lawsuits or forced binding arbitration.
    4. Unilateral changes to terms without notice.

    Contract Snippet:
    ---
    {text_chunk}
    ---
    """
    try:
        response = ollama.chat(
            model='llama3.2',
            messages=[{'role': 'user', 'content': prompt}],
            format=ContractAnalysis.model_json_schema(),
            options={'temperature': 0}
        )
        return ContractAnalysis.model_validate_json(response.message.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama error: {str(e)}")


@app.post("/analyze-text", response_model=ContractAnalysis)
async def analyze_text(request: TextRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text is empty.")
    return analyze_chunk_with_ollama(request.text)

@app.post("/analyze-pdf", response_model=ContractAnalysis)
async def analyze_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files supported.")

    extracted_text = ""
    with pdfplumber.open(io.BytesIO(await file.read())) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
        
    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from PDF.")

    return analyze_chunk_with_ollama(extracted_text[:3500])