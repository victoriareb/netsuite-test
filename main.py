from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi import Response
import httpx
import io

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.get("/image")
async def get_image():
    """
    Fetch a PNG image from the provided URL and stream it back with proper Content-Type headers.
    
    Args:
        url: The URL of the PNG image to fetch
        
    Returns:
        StreamingResponse: The image data with proper headers
    """
    try:
        url = "https://marketplace.canva.com/EAFEHtKS9p4/2/0/1131w/canva-blue-modern-creative-professional-company-invoice-KuVdlrcyWPE.jpg"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            
            # Check if the content is actually a PNG
            content_type = response.headers.get('content-type', '')
            if 'image/png' not in content_type:
                raise HTTPException(status_code=400, detail="URL does not point to a PNG image")
            
            # Stream the image data back
            return Response(
                content=response.content,
                media_type="image/png",
                headers={
                    "Content-Disposition": "inline",
                    "Cache-Control": "public, max-age=3600",
                    "Content-Length": str(len(response.content))  # 👈 ensure length
                }
            )
            
    except httpx.HTTPError as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch image: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

