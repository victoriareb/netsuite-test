from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
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
    Fetch an image (PNG, JPG, or JPEG) from the provided URL and stream it back with proper Content-Type headers.
    
    Returns:
        StreamingResponse: The image data with proper headers
    """
    try:
        url = "https://www.invoicesimple.com/wp-content/uploads/2024/08/simple-invoice-template-light-blue-en.jpg"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            
            # Check if the content is actually an image (PNG, JPG, or JPEG)
            content_type = response.headers.get('content-type', '').lower()
            if not any(img_type in content_type for img_type in ['image/png', 'image/jpeg', 'image/jpg']):
                raise HTTPException(status_code=400, detail="URL does not point to a supported image format (PNG, JPG, or JPEG)")
            
            # Determine the correct media type
            if 'image/png' in content_type:
                media_type = "image/png"
            elif 'image/jpeg' in content_type or 'image/jpg' in content_type:
                media_type = "image/jpeg"
            else:
                media_type = "image/jpeg"  # Default fallback
            
            # Stream the image data back
            return StreamingResponse(
                io.BytesIO(response.content),
                media_type=media_type,
                headers={
                    "Content-Disposition": "inline",
                    "Cache-Control": "public, max-age=3600"
                }
            )
            
    except httpx.HTTPError as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch image: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
