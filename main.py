from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid

from tools import process_report, _summarize_values, read_data_tool
from vector_db import add_analysis_result, search_similar

app = FastAPI(title="Blood Test Report Analyser")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Blood Test Report Analyser API is running"}

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: str = Form(default="Summarise my Blood Test Report and provide health recommendations"),
    user_id: str = Form(default="guest")
):
    if file is None:
        raise HTTPException(status_code=400, detail="No file uploaded")
    if file.filename == "":
        raise HTTPException(status_code=400, detail="Empty filename")

    # Save file locally
    file_id = str(uuid.uuid4())
    save_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    with open(save_path, "wb") as f:
        f.write(await file.read())

    # Read the text
    report_text = read_data_tool(save_path)

    if "Error" in report_text or not report_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from PDF")

    # Extract values
    values = _summarize_values(report_text)

    # --- Custom Query Handling ---
    query_lower = query.lower()
    filtered = []
    for val in values:
        if any(marker.lower() in query_lower for marker in ["hemoglobin", "glucose", "cholesterol", "vitamin d"]):
            if any(marker.lower() in val.lower() for marker in query_lower.split()):
                filtered.append(val)

    if filtered:
        analysis = "📋 Query-Specific Result:\n- " + "\n- ".join(filtered)
    else:
        # Fallback → full pipeline
        result = process_report(query, save_path)
        analysis = result["analysis"]

    # --- Save to Vector Database ---
    result_id = str(uuid.uuid4())
    add_analysis_result(
        result_id=result_id,
        query=query,
        analysis=analysis,
        metadata={
            "user_id": user_id,
            "file_name": file.filename,
            "file_path": save_path
        }
    )

    return {
        "id": result_id,
        "query": query,
        "file_processed": save_path,
        "analysis": analysis
    }

@app.get("/search")
async def search_reports(query: str, top_k: int = 3):
    results = search_similar(query, top_k)
    return results
