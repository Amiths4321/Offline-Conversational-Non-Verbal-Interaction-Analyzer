**Offline Conversational & Non-Verbal Interaction Analyzer**


An entirely offline, privacy-first backend service that analyzes video frames or photos taken during interviews, meetings, or clinical consultations. Using a remote vision-language model instance, it maps out non-verbal communication cues, subtle behavioral markers, eyebrow/jaw micro-expressions, postural dynamics, and cognitive load indicators, returning structured JSON data.

Features
100% Offline & Private: Zero external cloud or API dependencies (no OpenAI, no Anthropic). Highly suitable for sensitive corporate meetings or clinical consultations.

Advanced Vision Analytics: Powered by Qwen2.5-VL to track complex, microscopic human interaction variables simultaneously.

Safe-Fail Structural Schema: Automatically sanitizes model responses directly into clear, application-ready JSON.

FastAPI Backend: Ready-to-go endpoints with automatic browser UI documentation routing.

Architecture Flow
Client Interface: An uploaded session frame or close-up portrait image is received via FastAPI.

Base64 Payload Assembly: The image bytes are verified and converted safely into a Base64 string wrapper.

Internal Local Network Router: The application transmits the analytical payload seamlessly to your dedicated GPU endpoint running Ollama.

Structural Extraction parsing: The returned context is cleaned, evaluated for integrity, and delivered back as strict JSON.

Installation & Setup
1. Prerequisites
Ensure you have Python 3.10+ installed on your local environment.

2. Install Dependencies
Run the following command to set up the lightweight local ecosystem:

Bash
pip install fastapi uvicorn pillow
3. Verify Your Remote GPU Backend
Ensure your remote GPU server hosting the Ollama instance is accessible from your network machine:

Bash
ping 10.22.39.192
Note: Make sure the qwen2.5vl:latest model is pulled and actively serving on port 11434.

Running the Application
Launch the server from your terminal:

Bash
python interaction_app.py
Upon successful initialization, you will see confirmation logs in your terminal:

Plaintext
INFO:     Started server process [xxxxx]
INFO:     Uvicorn running on http://0.0.0.0:5002 (Press CTRL+C to quit)
Browser Interface & API Usage
Interactive Swagger UI Portal
Open your web browser and go directly to:

Plaintext
http://localhost:5002/
The application will automatically redirect you straight to the interactive testing engine.

Using the API Endpoint
Endpoint: POST /api/v1/analyze-interaction

Content-Type: multipart/form-data

Payload: file (Image file: .jpg, .jpeg, .png)

Sample JSON Response Output
JSON
{
  "status": "success",
  "analysis": {
    "primary_emotional_state": "Engaged",
    "micro_expressions": {
      "eyebrow_position": "Neutral",
      "jaw_tension": "Relaxed",
      "smile_authenticity": "Duchenne (Genuine)"
    },
    "body_language_markers": [
      "Open posture",
      "Slight forward postural lean towards the conversational partner",
      "Active hand gesturing confirming high engagement"
    ],
    "estimated_cognitive_load": "Medium",
    "interaction_rapport_rating": "Positive",
    "clinical_behavioral_notes": "Subject shows high attentive focus and genuine positive affect during the conversational sequence. No guarded or defensive markers observed."
  }
}
Configuration Tuning
If you need to tweak the core operational configurations, look at these parameters inside interaction_app.py:

OLLAMA_API_URL: Change this string if your remote GPU server host IP or port modifies.

temperature: Set to 0.2 by default. Lowering it makes the visual profiling completely deterministic; raising it slightly allows the system to synthesize more open-ended clinical interpretations.

port=5002: Ensures the runtime server stays isolated from standard network socket collisions.
