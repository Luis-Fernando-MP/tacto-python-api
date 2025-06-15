from typing import Optional
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
import asyncio
from edge_tts import Communicate

app = FastAPI()

# Diccionario de voces por país y género
VOICES = {
    "mujer": "es-CL-CatalinaNeural",
    "varon": "es-CL-LorenzoNeural",
}

@app.get("/")
async def root():
    return {"msg": "Usa /tts?text=Tu texto&vos=mujer|varon para obtener el mp3"}

@app.get("/tts")
async def tts_endpoint(
    text: str = Query(..., min_length=1),
    vos: str = Query("mujer", pattern="^(mujer|varon)$")
):
    output_path = "voz.mp3"
    voice = VOICES.get(vos, VOICES["mujer"])
    tts = Communicate(text=text, voice=voice)
    await tts.save(output_path)
    return FileResponse(output_path, media_type="audio/mpeg", filename="voz.mp3")
