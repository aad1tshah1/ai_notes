import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
client = Anthropic(api_key=api_key)


async def generate_meeting_notes(transcript: str) -> dict:
    system_prompt = """
    You generate structured meeting notes from transcripts.

    Return ONLY valid JSON. Do not include Markdown, headings, explanations, or text outside the JSON.

    The JSON must follow this exact structure:
    {
      "summary": "A concise summary of the meeting in 2-4 sentences.",
      "key_points": [
        "Important point 1",
        "Important point 2"
      ],
      "action_items": [
        "Action item 1",
        "Action item 2"
      ]
    }

    Rules:
    - If there are no action items, return an empty list.
    - Keep the summary useful but concise.
    - Do not invent details that are not in the transcript.
    - Return only valid JSON. Do not wrap the JSON in Markdown code fences.
    """

    message = client.messages.create(
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": transcript,
            }
        ],
        model="claude-haiku-4-5",
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