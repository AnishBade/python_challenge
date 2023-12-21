from fastapi import FastAPI, Request
import httpx
from starlette.responses import HTMLResponse

app = FastAPI()

@app.get("/{url:path}")
async def proxy(url: str, request: Request):
    # Reconstruct the full URL
    target_url = f"https://{url}"

    # Include query parameters if any
    if request.query_params:
        target_url += f"?{request.query_params}"

    # Make the request to the target URL
    async with httpx.AsyncClient() as client:
        resp = await client.get(target_url)

    # Return the content from the target URL
    return HTMLResponse(content=resp.content, status_code=resp.status_code)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
