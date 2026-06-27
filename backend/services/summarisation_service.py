import json
from anthropic import Anthropic
from core.config import config
from core.prompts import MEETING_NOTES_SYSTEM_PROMPT

client = Anthropic(api_key=config.anthropic_api_key)


async def generate_meeting_notes(transcript: str) -> dict:
    message = client.messages.create(
        max_tokens=config.anthropic_max_tokens,
        system=MEETING_NOTES_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": transcript,
            }
        ],
        model=config.anthropic_model,
    )

    generated_notes_text = message.content[0].text
    cleaned_notes_text = (
                            generated_notes_text
                            .replace("```json", "")
                            .replace("```", "")
                            .strip()
                        )
    parsed_notes = json.loads(cleaned_notes_text)

    return parsed_notes