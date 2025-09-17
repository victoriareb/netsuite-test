from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import httpx
import io
from fastapi import Response

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

@app.get("/ping")
def ping():
    return {"status": "ok"}


from fastapi import FastAPI, HTTPException, Response
import httpx

# app = FastAPI()
UPSTREAM = "https://static.vecteezy.com/system/resources/previews/020/716/214/non_2x/icon-online-invoice-illustration-invoice-icon-free-png.png"

@app.head("/image.png")
async def head_image():
    async with httpx.AsyncClient(follow_redirects=True, timeout=20.0) as client:
        r = await client.head(UPSTREAM)
        r.raise_for_status()
    ct = r.headers.get("content-type", "").split(";",1)[0].strip()
    if not ct.startswith("image/"):
        raise HTTPException(status_code=400, detail="Upstream not an image")
    headers = {
        "Content-Type": ct,
        "Content-Length": r.headers.get("content-length", ""),
        "Content-Disposition": 'inline; filename="invoice.png"',
        "Cache-Control": "public, max-age=3600",
    }
    return Response(content=b"", headers=headers)

@app.get("/image.png")
async def get_image():
    async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
        r = await client.get(UPSTREAM)
        r.raise_for_status()
    ct = r.headers.get("content-type", "").split(";",1)[0].strip()
    if not ct.startswith("image/"):
        raise HTTPException(status_code=400, detail="Upstream not an image")
    content = r.content  # small images OK; ensures Content-Length can be set
    headers = {
        "Content-Disposition": 'inline; filename="invoice.png"',
        "Cache-Control": "public, max-age=3600",
        "Content-Length": str(len(content)),
    }
    return Response(content=content, media_type=ct, headers=headers)
