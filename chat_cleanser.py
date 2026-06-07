import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Automatically look for the .env file and load its variables into memory
load_dotenv()

def cleanse_text(raw_text: str) -> str:
    try:
        # The client will now securely grab the key from your .env file
        client = Anthropic()
    except Exception as e:
        return f"Error initializing client. Check your .env file! Details: {e}"

    system_prompt = """
    You are a specialized Text Cleansing and Moderation Assistant. Your primary task is to sanitize input text by censoring explicit slang words, removing/censoring offensive emojis, and detecting high-level negative intent (toxic phrases), transforming them according to strict formatting rules.

    # Rules & Logic
    1. Direct Slang Censorship (Words):
       - Identify explicit or profane words (e.g., "ass", "fuck", "bitch", etc.).
       - Replace the entire word with exactly three asterisks: ***
       - Preserve surrounding punctuation and spacing.

    2. Offensive Emoji Censorship:
       - Identify offensive or derogatory emojis (e.g., middle finger variations like 🖕🏻).
       - Replace each offensive emoji with exactly three asterisks: ***

    3. Intention & Phrase Redaction:
       - Detect complete phrases or sentences that carry explicit bad intentions or directed toxicity (e.g., "fuck you", "go screw yourself").
       - Replace the specific toxic phrase/sentence with the exact string: [slang uses]

    # Output Requirement
    - Output ONLY the sanitized text. 
    - Do not add any conversational filler, explanations, or introductory text.
    """

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            temperature=0.0,
            system=system_prompt,
            messages=[{"role": "user", "content": raw_text}]
        )
        return message.content[0].text
    except Exception as e:
        return f"API Error: {e}"

if __name__ == "__main__":
    print("--- Chat Cleanser Active (Secure Mode) ---")
    test_inputs = [
        "Hey, what the fuck is your problem?",
        "Shut up 🖕🏻",
        "Get out of here, fuck you."
    ]
    for text in test_inputs:
        print(f"\nInput:  {text}")
        print(f"Output: {cleanse_text(text)}")