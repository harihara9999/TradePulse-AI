from pydantic import BaseModel, Field

class AnalysisRequest(BaseModel):
    sector: str = Field(..., min_length=2, max_length=50, description="The market sector to analyze (e.g., 'pharmaceuticals')")

class AnalysisResponse(BaseModel):
    sector: str
    report: str
    status: str = "success"
