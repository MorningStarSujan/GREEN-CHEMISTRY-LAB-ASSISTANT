import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

from utils.chat_memory import add_message, get_context
from utils.cache import get_cached_response, save_cached_response
from utils.ai_identity import AI_IDENTITY

# -----------------------------
# Load Environment
# -----------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

print("\n========== API KEY CHECK ==========")
print(API_KEY)
print("===================================\n")

if not API_KEY:
    raise ValueError("Gemini API Key not found.")

client = genai.Client(api_key=API_KEY)


# -----------------------------
# Build Prompt
# -----------------------------


def build_prompt(question, context=None):

    prompt = ""

    if context:
        prompt += f"""
Local Chemical Information

{context}

----------------------------------------

"""

    conversation = get_context()

    prompt += f"""
Conversation History

{conversation}

----------------------------------------

Current User Question

{question}
"""

    return prompt


# -----------------------------
# Normal Gemini Response
# -----------------------------


def ask_gemini(question, context=None):

    cached = get_cached_response(question)

    if cached:
        return cached

    prompt = build_prompt(question, context)

    try:

        start = time.time()

        response = client.models.generate_content_stream(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(system_instruction=AI_IDENTITY),
        )

        answer = ""

        for chunk in response:

            if chunk.text:
                answer += chunk.text

        print(f"Gemini Response Time: {time.time() - start:.2f}s")

    except Exception as e:

        print("\n========== GEMINI ERROR ==========")
        print(type(e))
        print(e)
        print("==================================\n")

        return (
            "⚠️ Gemini is temporarily unavailable.\n\n" "Please try again in a moment."
        )

    save_cached_response(question, answer)

    add_message("User", question)
    add_message("Assistant", answer)

    return answer


# -----------------------------
# Streaming Gemini Response
# -----------------------------


def ask_gemini_stream(question, context=None):

    prompt = build_prompt(question, context)

    try:

        response = client.models.generate_content_stream(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(system_instruction=AI_IDENTITY),
        )

        full_answer = ""

        for chunk in response:

            if chunk.text:
                full_answer += chunk.text
                yield chunk.text

        save_cached_response(question, full_answer)

        add_message("User", question)
        add_message("Assistant", full_answer)

    except Exception as e:

        print("\n========== GEMINI ERROR ==========")
        print(type(e))
        print(e)
        print("==================================\n")

        yield "⚠️ Gemini is temporarily unavailable.\nPlease try again in a moment."
