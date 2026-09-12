import re
import json
import random
from datetime import datetime

# ============================================================
# AI REGISTRATION ASSISTANT
# Task ID: AI-SS-001
# ============================================================

class RegistrationAssistant:

    def __init__(self):
        self.user_data = {}
        self.intents = self.load_intents()

    # --------------------------------------------------------
    # INTENTS
    # --------------------------------------------------------
    def load_intents(self):
        return {
            "greeting": {
                "patterns": [
                    "hi", "hello", "hey", "good morning",
                    "good afternoon", "good evening"
                ],
                "response": "Hello! 👋 Welcome to the AI Registration Assistant."
            },

            "register": {
                "patterns": [
                    "register", "registration", "apply",
                    "sign up", "join", "enroll"
                ],
                "response": "Great! I'll help you complete your registration."
            },

            "help": {
                "patterns": [
                    "help", "support", "assist", "guide"
                ],
                "response": (
                    "I can help you with:\n"
                    "1. Internship registration\n"
                    "2. Eligibility information\n"
                    "3. Required details\n"
                    "4. Registration confirmation"
                )
            },

            "eligibility": {
                "patterns": [
                    "eligible", "eligibility", "qualification",
                    "qualify", "requirements"
                ],
                "response": (
                    "The registration assistant can collect your "
                    "name, email, field of study, and experience."
                )
            },

            "internship": {
                "patterns": [
                    "internship", "intern", "training",
                    "course", "program"
                ],
                "response": (
                    "This is an AI & Data Science internship "
                    "registration assistant."
                )
            },

            "thank_you": {
                "patterns": [
                    "thanks", "thank you", "thank"
                ],
                "response": "You're welcome! 😊"
            },

            "bye": {
                "patterns": [
                    "bye", "goodbye", "exit", "quit"
                ],
                "response": "Thank you for using the AI Registration Assistant. Goodbye! 👋"
            }
        }

    # --------------------------------------------------------
    # NLP PREPROCESSING
    # --------------------------------------------------------
    def preprocess_text(self, text):
        text = text.lower()
        text = re.sub(r"[^a-zA-Z0-9@\s.]", "", text)

        words = text.split()

        # Simple stop-word removal
        stop_words = {
            "the", "is", "am", "are", "a", "an",
            "i", "my", "to", "for", "and", "of",
            "in", "on", "please"
        }

        words = [word for word in words if word not in stop_words]

        return words

    # --------------------------------------------------------
    # INTENT CLASSIFICATION
    # --------------------------------------------------------
    def classify_intent(self, text):

        text_lower = text.lower()

        for intent, data in self.intents.items():

            for pattern in data["patterns"]:

                if re.search(r"\b" + re.escape(pattern) + r"\b", text_lower):
                    return intent

        return "unknown"

    # --------------------------------------------------------
    # ENTITY EXTRACTION
    # --------------------------------------------------------
    def extract_entities(self, text):

        entities = {}

        # Email
        email_match = re.search(
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            text
        )

        if email_match:
            entities["email"] = email_match.group()

        # Name
        name_match = re.search(
            r"(?:my name is|i am|i'm)\s+([a-zA-Z ]+)",
            text,
            re.IGNORECASE
        )

        if name_match:
            name = name_match.group(1).strip()
            name = re.split(
                r"\b(?:and|my|email|i|study)\b",
                name,
                flags=re.IGNORECASE
            )[0].strip()

            if name:
                entities["name"] = name.title()

        # Field of study
        fields = [
            "computer science",
            "computer engineering",
            "information technology",
            "data science",
            "artificial intelligence",
            "electronics",
            "mechanical engineering",
            "civil engineering"
        ]

        text_lower = text.lower()

        for field in fields:
            if field in text_lower:
                entities["field"] = field.title()
                break

        # Experience
        experience_levels = [
            "beginner",
            "intermediate",
            "advanced",
            "fresher",
            "experienced"
        ]

        for level in experience_levels:
            if level in text_lower:
                entities["experience"] = level.title()
                break

        return entities

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------
    def validate_email(self, email):

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        return re.match(pattern, email) is not None

    def validate_name(self, name):

        return (
            len(name.strip()) >= 2
            and all(character.isalpha() or character.isspace()
                    for character in name)
        )

    # --------------------------------------------------------
    # SAVE REGISTRATION
    # --------------------------------------------------------
    def save_registration(self):

        self.user_data["registration_id"] = (
            "REG" + str(random.randint(1000, 9999))
        )

        self.user_data["registered_at"] = (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        try:
            with open("registrations.json", "r") as file:
                registrations = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            registrations = []

        registrations.append(self.user_data.copy())

        with open("registrations.json", "w") as file:
            json.dump(registrations, file, indent=4)

    # --------------------------------------------------------
    # REGISTRATION PROCESS
    # --------------------------------------------------------
    def registration_process(self):

        print("\nAssistant: Let's complete your registration! 🚀")

        # Name
        while True:

            name = input("\nAssistant: What is your full name?\nYou: ").strip()

            if self.validate_name(name):
                self.user_data["name"] = name.title()
                break

            print("Assistant: Please enter a valid name.")

        # Email
        while True:

            email = input(
                "\nAssistant: What is your email address?\nYou: "
            ).strip()

            if self.validate_email(email):
                self.user_data["email"] = email
                break

            print("Assistant: Please enter a valid email address.")

        # Field
        print(
            "\nAssistant: What is your field of study?"
        )

        field = input("You: ").strip()

        while not field:
            print("Assistant: Please enter your field of study.")
            field = input("You: ").strip()

        self.user_data["field"] = field.title()

        # Experience
        print(
            "\nAssistant: What is your programming experience?"
        )

        print("Examples: Beginner, Intermediate, Advanced, Fresher")

        experience = input("You: ").strip()

        while not experience:
            print("Assistant: Please enter your experience level.")
            experience = input("You: ").strip()

        self.user_data["experience"] = experience.title()

        # Confirmation
        print("\n" + "=" * 50)
        print("           REGISTRATION SUMMARY")
        print("=" * 50)

        print(f"Name       : {self.user_data['name']}")
        print(f"Email      : {self.user_data['email']}")
        print(f"Field      : {self.user_data['field']}")
        print(f"Experience : {self.user_data['experience']}")

        print("=" * 50)

        confirm = input(
            "Assistant: Do you want to confirm your registration? (yes/no)\nYou: "
        ).strip().lower()

        if confirm in ["yes", "y"]:

            self.save_registration()

            print("\n" + "=" * 50)
            print("       ✅ REGISTRATION SUCCESSFUL!")
            print("=" * 50)

            print(
                f"Registration ID: "
                f"{self.user_data['registration_id']}"
            )

            print(
                f"Registered At: "
                f"{self.user_data['registered_at']}"
            )

            print("=" * 50)

        else:

            print("\nAssistant: Registration cancelled.")

    # --------------------------------------------------------
    # CHATBOT
    # --------------------------------------------------------
    def chat(self):

        print("\n" + "=" * 60)
        print("          🤖 AI REGISTRATION ASSISTANT")
        print("=" * 60)

        print(
            "Assistant: Hello! I am your AI Registration Assistant."
        )

        print(
            "Assistant: Type 'help' to see what I can do."
        )

        print(
            "Assistant: Type 'register' to start registration."
        )

        print(
            "Assistant: Type 'bye' to exit."
        )

        print("=" * 60)

        while True:

            user_input = input("\nYou: ").strip()

            if not user_input:
                print("Assistant: Please enter a message.")
                continue

            # Extract entities from every message
            entities = self.extract_entities(user_input)

            if entities:
                self.user_data.update(entities)

            # Check exit
            intent = self.classify_intent(user_input)

            if intent == "bye":
                print("\nAssistant:", self.intents["bye"]["response"])
                break

            # Registration
            if intent == "register":

                self.registration_process()

                continue

            # Show extracted information
            if entities:

                print("\nAssistant: I understood:")

                for key, value in entities.items():
                    print(f"  {key.title()}: {value}")

            # Normal response
            if intent in self.intents:

                print(
                    "\nAssistant:",
                    self.intents[intent]["response"]
                )

            else:

                print(
                    "\nAssistant: I'm not sure I understood that."
                )

                print(
                    "Assistant: You can ask about registration, "
                    "eligibility, internship details, or help."
                )


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    assistant = RegistrationAssistant()

    assistant.chat()