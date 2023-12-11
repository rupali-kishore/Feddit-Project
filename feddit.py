from fastapi import FastAPI, HTTPException
import uvicorn
from feddit_controller import SubfedditController
from util.logger_util import Logger

# Get logger for the current module
logger = Logger().get_logger(__name__)

app = FastAPI(debug=True)

@app.get("/subfeddit/_recent_comments")
async def get_subfeddit_recent_comments(title: str):
    """API to fetch recent comment by title

    Args:
        title (str): Input title

    Raises:
        HTTPException: Bad Request
        HTTPException: Internal Server Error

    Returns:
        dict: Response Json
    """
    try:
        if not title:
            raise HTTPException(status_code=400, detail="Bad Request: Title missing")
        logger.info("Fetching recent comments")
        result = SubfedditController().process_request_recent_comments(title)
        logger.info("Processed recent comments successfully")
        return result
    except Exception as e:
        logger.error(f"Error processing recent comments: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/subfeddit/_comments_date_range")
async def get_subfeddit_comments_date_range(title: str, start: str, end: str):
    """API to fetch comment between given period

    Args:
        title (str): Input title
        start (str): Input start date (YYYY/MM/DD)
        end (str): Input end date (YYYY/MM/DD)

    Raises:
        HTTPException: Bad Request
        HTTPException: Bad Reqeust
        HTTPException: Internal Server Error

    Returns:
        _type_: _description_
    """
    try:
        if not title:
            raise HTTPException(status_code=400, detail="Bad Request: Title missing")
        if not start or not end:
            raise HTTPException(status_code=400, detail="Bad Request: Either start date, end date or both are missing")
        logger.info("Fetching recent comments")
        result = SubfedditController().process_request_comments_date_range(title, start, end)
        logger.info("Processed comments date range successfully")
        return result
    except Exception as e:
        logger.error(f"Error processing comments date range: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
