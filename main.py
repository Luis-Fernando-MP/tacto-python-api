from typing import Optional
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse

import asyncio
from edge_tts import Communicate

app = FastAPI()

@app.get("/")
async def root():
    return {"msg": "Hola, usa /tts?text=Tu texto para obtener el mp3"}

@app.get("/tts")
async def tts_endpoint(text: str = Query(..., min_length=1)):
    output_path = "voz.mp3"
    tts = Communicate(text=text, voice="es-CL-LorenzoNeural")
    await tts.save(output_path)
    return FileResponse(output_path, media_type="audio/mpeg", filename="voz.mp3")