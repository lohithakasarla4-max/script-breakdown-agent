import os
import json
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Please create a .env file and add your Gemini API key."
    )

# Create Gemini client
client = genai.Client(api_key=API_KEY)

# Current stable model with free-tier availability
MODEL_NAME = "gemini-3.6-flash"


def analyze_script_scene(script_text: str):
    """
    Analyze a screenplay/script and return structured
    production and storyboard information.
    """

    prompt = f"""
You are an expert Hollywood Assistant Director,
Script Supervisor, Storyboard Artist, and Film Production Planner.

Analyze the following screenplay.

Your job is to break the screenplay into useful
production and storyboard information.

Return ONLY valid JSON.

Use EXACTLY this structure:

{{
    "project_title": "Title if available",
    "total_scenes": 0,

    "scenes": [
        {{
            "scene_number": 1,
            "scene_heading": "INT./EXT. LOCATION - TIME",
            "location": "Detailed location",
            "interior_exterior": "INT or EXT",
            "time_of_day": "DAY/NIGHT/SUNSET/etc",

            "characters": [
                "Character 1",
                "Character 2"
            ],

            "action_summary": "Short summary of what happens",

            "dialogue_summary": "Important dialogue or conversation summary",

            "props": [
                "Important props"
            ],

            "costume_notes": [
                "Important costume information"
            ],

            "vehicles": [
                "Vehicles required"
            ],

            "sound_effects": [
                "Important sound effects"
            ],

            "music": [
                "Music or score suggestions"
            ],

            "visual_style": "Description of the visual style",

            "camera_shots": [
                {{
                    "shot": "Wide Shot",
                    "description": "What should be visible",
                    "camera_movement": "Static/Pan/Tilt/Dolly/Tracking/etc",
                    "angle": "Eye level/Low angle/High angle/etc"
                }}
            ],

            "storyboard": [
                {{
                    "panel": 1,
                    "shot_type": "Wide/Medium/Close-up/etc",
                    "visual_description": "What the storyboard frame should show",
                    "characters_visible": [
                        "Character names"
                    ],
                    "action": "Action happening in the frame",
                    "dialogue": "Dialogue if relevant",
                    "camera": "Camera position and movement"
                }}
            ],

            "production_requirements": [
                "Important requirements for filming"
            ],

            "continuity_notes": [
                "Continuity information"
            ]
        }}
    ],

    "production_summary": {{
        "locations": [],
        "characters": [],
        "props": [],
        "vehicles": [],
        "costumes": [],
        "special_requirements": []
    }}
}}

IMPORTANT RULES:

1. Do not invent information that is not reasonably supported
   by the screenplay.

2. If information is not available, use an empty list []
   or "Not specified".

3. Preserve character names exactly when possible.

4. Separate every scene correctly.

5. Identify INT/EXT and time of day from scene headings.

6. Extract important props.

7. Extract important costume requirements.

8. Extract vehicles.

9. Extract sound effects.

10. Identify useful camera shots.

11. Create practical storyboard panels for each important
    visual beat.

12. Keep the JSON valid.

13. Do not use Markdown.

14. Do not put ```json around the response.

SCREENPLAY:

{script_text}
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        text = response.text.strip()

        # Remove accidental Markdown code fences
        if text.startswith("```json"):
            text = text[7:]

        if text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        # Validate JSON
        data = json.loads(text)

        return data

    except json.JSONDecodeError as e:
        return {
            "error": "Gemini returned invalid JSON.",
            "details": str(e),
            "raw_response": text if "text" in locals() else ""
        }

    except Exception as e:
        return {
            "error": "Gemini API request failed.",
            "details": str(e)
        }


def analyze_script(script_text: str):
    """
    Main function used by the Streamlit application.
    """

    if not script_text or not script_text.strip():
        return {
            "error": "Please enter a screenplay first."
        }

    return analyze_script_scene(script_text)