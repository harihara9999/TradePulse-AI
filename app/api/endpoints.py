from fastapi import APIRouter, Depends, HTTPException, Request, status, Response
from app.services.scraper import collect_market_data
from app.services.ai import generate_analysis_report
from app.core.security import get_api_key, limiter
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/analyze/{sector}")
@limiter.limit("5/minute")
async def analyze_sector(
    request: Request,
    sector: str,
    api_key: str = Depends(get_api_key)
):
    """
    Analyzes the given sector and returns a structured markdown report.
    This endpoint is rate-limited.
    """
    if len(sector) < 2 or len(sector) > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sector name must be between 2 and 50 characters."
        )
    
    if not sector.isalnum() and not all(x.isalnum() or x.isspace() for x in sector):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sector name can only contain alphanumeric characters and spaces."
        )

    try:
        # Step 1: Collect market data
        collected_data = await collect_market_data(sector)
        
        # Step 2: Generate analysis report using AI
        report_markdown = await generate_analysis_report(sector, collected_data)
        
        # return AnalysisResponse(sector=sector, report=report_markdown)
        return Response(
            content=report_markdown, 
            media_type="text/markdown",
            headers={"Content-Disposition": f'attachment; filename="{sector}_market_analysis.md"'}
        )

    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ve)
        )
    except Exception as e:
        logger.error(f"Error processing analysis for {sector}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while generating the report. Please try again later."
        )
