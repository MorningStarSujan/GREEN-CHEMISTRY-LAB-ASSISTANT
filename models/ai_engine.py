from utils.chemical_loader import load_all_chemicals
from utils.knowledge_base import KNOWLEDGE
from utils.response_formatter import (
    format_chemical,
    format_green_chemistry,
    format_lab_safety,
)
from utils.gemini_service import ask_gemini

FORMATTERS = {
    "green_chemistry": format_green_chemistry,
    "lab_safety": format_lab_safety,
}


class AIEngine:

    def __init__(self):
        self.chemicals = load_all_chemicals()

    def get_response(self, question):

        question = question.lower().strip()

        # Search Knowledge Base
        for topic in KNOWLEDGE.values():
            for keyword in topic["keywords"]:
                if keyword in question:
                    formatter = FORMATTERS.get(topic["formatter"])
                    if formatter:
                        return formatter(topic)

        # Search Chemical Database
        for chemical in self.chemicals:

            name = chemical.get("name", "").lower()
            formula = chemical.get("formula", "").lower()
            aliases = [alias.lower() for alias in chemical.get("aliases", [])]

            context = f"""
Name: {chemical.get('name')}
Formula: {chemical.get('formula')}
Category: {chemical.get('category')}
Description: {chemical.get('description')}
Hazards: {chemical.get('hazards')}
Storage: {chemical.get('storage')}
Disposal: {chemical.get('disposal')}
Green Alternative: {chemical.get('green_alternative')}
"""

            # Match full chemical name
            if name and name in question:
                return format_chemical(chemical)

            # Match formula
            if formula and formula in question:
                return ask_gemini(question, context)

            # Match aliases
            for alias in aliases:
                if alias in question:
                    return ask_gemini(question, context)

            # Match partial words
            for word in name.split():
                if len(word) > 3 and word in question:
                    return ask_gemini(question, context)

        # If nothing was found locally, ask Gemini
        try:
            return ask_gemini(question)

        except Exception as e:
            print("Gemini Error:", e)
            return "❌ Sorry, I couldn't answer your question because the AI service is currently unavailable."
