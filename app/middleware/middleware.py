from fastapi import Request
import time

async def time_counter(request:Request,call_next):
    start = time.time()
    response = await call_next(request)
    time_taken = time.time()-start
    response.headers["X-Process-Time"] = str(time_taken)
    return response
