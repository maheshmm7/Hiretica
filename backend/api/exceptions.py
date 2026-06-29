from fastapi import Request
from fastapi.responses import JSONResponse


class PipelineError(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code


async def pipeline_error_handler(request: Request, exc: PipelineError):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.message})
