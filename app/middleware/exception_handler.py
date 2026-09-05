from fastapi import Request
from fastapi.responses import JSONResponse

async def exception_handler(request:Request,call_next):
    try:
        response = await call_next(request)
        return response

    except Exception as exc:
        print(exc)
        return JSONResponse(
            status_code=500,
            content={"detail":"Internal Server Error!!"}
        )