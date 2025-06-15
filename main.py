from typing import Optional
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
import asyncio
from edge_tts import Communicate

app = FastAPI()

VOICES = {
    "pe": {"mujer": "es-PE-CamilaNeural", "varon": "es-PE-AlexNeural"},
    "mx": {"mujer": "es-MX-DaliaNeural", "varon": "es-MX-JorgeNeural"},
    "ar": {"mujer": "es-AR-ElenaNeural", "varon": "es-AR-TomasNeural"},
    "cl": {"mujer": "es-CL-CatalinaNeural", "varon": "es-CL-LorenzoNeural"},
}

@app.get("/")
async def root():
    return {
        "msg": "Usa /tts?text=Tu texto&vos=mujer|varon&pais=pe|mx|ar|cl para obtener el mp3"
    }

@app.get("/tts")
async def tts_endpoint(
    text: str = Query(..., min_length=1),
    vos: str = Query("mujer", pattern="^(mujer|varon)$"),
    pais: str = Query("pe", pattern="^(pe|mx|ar|cl)$"),
):
    voice = VOICES[pais][vos]
    output_path = "voz.mp3"
    tts = Communicate(text=text, voice=voice)
    await tts.save(output_path)
    return FileResponse(output_path, media_type="audio/mpeg", filename="voz.mp3")
