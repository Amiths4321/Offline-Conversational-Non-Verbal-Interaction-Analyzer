import io
import json
import base64
import urllib.request
import urllib.error
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from PIL import Image

app = FastAPI(title="Offline Conversational & Non-Verbal Interaction Analyzer")

OLLAMA_API_URL = "http://10.22.39.192:11434/api/chat"
MODEL_NAME = "qwen2.5vl:latest"

# Structured schema for social perception and behavioral tracking
BEHAVIOR_SCHEMA = """
{
    "primary_emotional_state": "Engaged / Defensive / Anxious / Neutral / Fatigued",
    "micro_expressions": {
        "eyebrow_position": "Raised / Furrowed / Neutral",
        "jaw_tension": "High / Relaxed",
        "smile_authenticity": "Duchenne (Genuine) / Social (Forced) / None"
    },
    "body_language_markers": [
        "e.g., Open posture, Crossed arms, Hand-to-face touching, Postural lean back"
    ],
    "estimated_cognitive_load": "Low / Medium / High",
    "interaction_rapport_rating": "Positive / Strained / Guarded / Attentive",
    "clinical_behavioral_notes": "A brief structural synthesis of observed behavioral patterns and social cues."
}
"""

@app.get("/")
async def root():
    # Direct automatic redirection to avoid "Not Found" browser errors
    return RedirectResponse(url="/docs")

@app.post("/api/v1/analyze-interaction")
async def analyze_interaction(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="The uploaded file must be an image.")

    try:
        image_bytes = await file.read()
        
        # Verify image health
        try:
            Image.open(io.BytesIO(image_bytes)).verify()
        except Exception:
            raise HTTPException(status_code=400, detail="Corrupted image file.")

        base64_image = base64.b64encode(image_bytes).decode('utf-8')

        # System prompt focused purely on objective social perception and structural tracking
        prompt = (
            "You are an expert behavioral scientist and non-verbal communication system. "
            "Analyze this interaction frame objectively to map expressions, posture, rapport, and subtle human behavioral indicators. "
            f"Output strictly valid JSON conforming exactly to this schema structural layout:\n{BEHAVIOR_SCHEMA}\n"
            "Do not output markdown code formatting, text wrappers, or explanatory preambles. Output raw JSON only."
        )

        payload = {
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                    "images": [base64_image]
                }
            ],
            "stream": False,
            "options": {
                "temperature": 0.2  # Balanced slightly for subtle visual inference tracking
            }
        }

        # Transmit payload over internal network link
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            OLLAMA_API_URL, 
            data=data, 
            headers={"Content-Type": "application/json"}
        )

        with urllib.request.urlopen(req, timeout=60) as response:
            res_body = json.loads(response.read().decode("utf-8"))
            output_text = res_body.get("message", {}).get("content", "").strip()

        # Clean accidental markdown formatting strings
        if output_text.startswith("```json"):
            output_text = output_text.split("```json")[1].split("```")[0].strip()
        elif output_text.startswith("```"):
            output_text = output_text.split("```")[1].split("```")[0].strip()

        behavioral_data = json.loads(output_text)
        return JSONResponse(content={"status": "success", "analysis": behavioral_data})

    except urllib.error.URLError as ue:
        return JSONResponse(
            status_code=503, 
            content={"status": "error", "message": "Unable to communicate with remote GPU host.", "details": str(ue.reason)}
        )
    except json.JSONDecodeError:
        return JSONResponse(
            status_code=422, 
            content={"status": "error", "message": "Failed to parse behavioral analytics string into JSON.", "raw_output": output_text}
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

if __name__ == "__main__":
    import uvicorn
    # Launched on alternative port 5002 to ensure zero socket interface overlaps
    uvicorn.run(app, host="0.0.0.0", port=5002)