import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from utils.chat_memory import add_message, get_context
from utils.cache import get_cached_response, save_cached_response

# Load .env file
load_dotenv()

# Read API key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Gemini API Key not found. Check your .env file.")

# Create Gemini client
client = genai.Client(api_key=API_KEY)


def ask_gemini(question, context=None):
    """
    Ask Gemini using optional local chemistry context.
    """

    # Block non-chemistry questions
    chemistry_keywords = [
        "chemistry",
        "chemical",
        "acid",
        "base",
        "lab",
        "laboratory",
        "experiment",
        "reaction",
        "molecule",
        "atom",
        "compound",
        "green chemistry",
        "safety",
        "hazard",
        "ppe",
        "disposal",
        "solvent",
        "beaker",
        "flask",
        "titration",
        "ph",
        "alkali",
        "salt",
        "organic",
        "inorganic",
        "element",
        "periodic",
        "solution",
        "mixture",
        "acetone",
        "ethanol",
        "methanol",
        "sulfuric",
        "hydrochloric",
        "nitric",
        "sodium",
        "potassium",
        "calcium",
        "hydrogen",
        "oxygen",
        "carbon",
    ]

    question = question.strip()
    question_lower = question.lower()

    # Check cache first
    cached = get_cached_response(question)

    if cached:
        return cached

    if not any(keyword in question_lower for keyword in chemistry_keywords):

        return (
            "❌ Sorry! I am the Green Chemistry Lab Assistant.\n\n"
            "I can only answer questions related to:\n"
            "• Chemistry\n"
            "• Laboratory Safety\n"
            "• Green Chemistry\n"
            "• Chemical Handling\n"
            "• Experiments\n"
            "• Waste Disposal\n"
            "• Environmental Sustainability"
        )

    system_prompt = """
You are Green Chemistry Lab Assistant.

You are an expert in:
• Chemistry
• Green Chemistry
• Laboratory Safety
• Chemical Handling
• Waste Disposal
• Environmental Sustainability

Rules:

1. Answer ONLY chemistry-related questions.
2. If local chemical information is provided, ALWAYS use it as your primary source.
3. Expand the local information instead of replacing it.
4. Always include:
   • Overview
   • Safety Information
   • Green Chemistry Tip
5. Keep answers clear and student-friendly.
6. Use proper headings and bullet points.
7. Never use LaTeX.
8. Write chemical formulas in plain text.
   Example:
   - H2SO4
   - NaOH
   - CH3COCH3
"""

    prompt = ""

    # Add local database information
    if context:
        prompt += f"""
Local Chemical Information

{context}

------------------------

"""

    # Add previous conversation
    conversation = get_context()

    prompt += f"""
Conversation History

{conversation}

------------------------

Current User Question

{question}
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(system_instruction=system_prompt),
        )
    except Exception as e:
        print("Gemini Error:", e)

        return (
            "⚠️ AI service is temporarily unavailable.\n\n"
            "The Gemini API request limit has been reached.\n"
            "Please wait about a minute and try again."
        )

    # Save conversation
    answer = response.text

    # Save in cache
    save_cached_response(question, answer)

    # Save conversation
    add_message("User", question)
    add_message("Assistant", answer)

    return answer
