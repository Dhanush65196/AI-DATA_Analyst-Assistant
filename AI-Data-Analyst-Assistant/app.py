"""
Main application file for AI Data Analyst Assistant
"""
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from utils.data_loader import DataLoader
from utils.analyzer import DataAnalyzer
from utils.llm_helper import LLMHelper

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Data Analyst Assistant")

# Initialize components
data_loader = DataLoader()
analyzer = DataAnalyzer()
llm_helper = LLMHelper()


@app.get("/")
def read_root():
    """Root endpoint"""
    return {"message": "Welcome to AI Data Analyst Assistant"}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/analyze")
def analyze_data(file_path: str):
    """Analyze uploaded data file"""
    try:
        # Load data
        df = data_loader.load_data(file_path)
        
        # Analyze data
        analysis_results = analyzer.analyze(df)
        
        # Get AI insights
        insights = llm_helper.get_insights(analysis_results)
        
        return {
            "status": "success",
            "analysis": analysis_results,
            "insights": insights
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
