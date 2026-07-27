from utils.chemical_loader import load_all_chemicals
from utils.knowledge_base import KNOWLEDGE
from utils.response_formatter import (
    format_chemical,
    format_green_chemistry,
    format_lab_safety,
)

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

            # Match full chemical name
            if name in question:
                return format_chemical(chemical)

            # Match formula
            if formula and formula in question:
                return format_chemical(chemical)

            # Match aliases
            for alias in aliases:
                if alias in question:
                    return format_chemical(chemical)

            # Match partial words
            for word in name.split():
                if len(word) > 3 and word in question:
                    return format_chemical(chemical)

        return (
            "❌ Sorry, I couldn't find that chemical.\n\n"
            "You can ask me about:\n\n"
            "• Sulfuric Acid\n"
            "• Hydrochloric Acid\n"
            "• Sodium Hydroxide\n"
            "• Ethanol\n"
            "• Acetone\n"
            "• Benzene\n"
            "• Oxygen\n"
            "• Hydrogen Peroxide\n\n"
            "You can also search using:\n"
            "• Chemical Name\n"
            "• Formula\n"
            "• Alias\n"
            "• Partial Name"
        )
