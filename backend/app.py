import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
# Natively unlock full cross-origin communications for your local browser windows
CORS(app, resources={r"/*": {"origins": "*"}})

# ---------------------------------------------------------------------
# SAFE SYSTEM KEY RESOLVER (Checks folder layout directories)
# ---------------------------------------------------------------------
API_KEY = os.environ.get("GEMINI_API_KEY", "").strip().strip("'\"")

if not API_KEY:
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if "GEMINI_API_KEY" in line and "=" in line:
                    API_KEY = line.split("=", 1)[1].strip().strip("'\"")

# Safeguard key fallback tracking
client = genai.Client(api_key=API_KEY if API_KEY else "MISSING_KEY")

@app.route('/', methods=['POST'])
def generate_flashcards():
    try:
        request_data = request.get_json()
        user_notes = request_data.get("notes", "")
        
        if not user_notes:
            return jsonify({"success": False, "error": "No notes provided text"}), 400

        # Official Google API call targeting the active model
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=(
                "Transform the following raw study notes into a structured JSON array of flashcards. "
                "Each flashcard object must contain exactly two keys: 'question' and 'answer'. "
                "Output ONLY raw valid JSON text, no markdown code blocks:\n\n"
                f"{user_notes}"
            )
        )
        
        # Strip away potential markdown syntax wrappers cleanly
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        flashcards_data = json.loads(clean_text)
        
        return jsonify({"success": True, "flashcards": flashcards_data})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Flask Server running perfectly on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)
