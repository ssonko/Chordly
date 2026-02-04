import os
import json
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv(
    dotenv_path=os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../.env")
    ),
    override=True
)

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


async def search_song(query: str) -> dict:
    prompt = f"""
You are a music transcription assistant.

CRITICAL FORMAT RULES (DO NOT BREAK):
- NEVER return chord-only lines.
- Each lyric line MUST contain all its chords in ONE array.
- One lyric line = one chords array.
- DO NOT split chords across multiple lines.
- DO NOT return empty lyrics.

GOOD EXAMPLE:
{{
  "chords": ["G", "G7", "C", "G"],
  "lyrics": "Amazing Grace, how sweet the sound"
}}

BAD EXAMPLE (FORBIDDEN):
{{ "chords": ["G"], "lyrics": "" }}

LEGAL RULES:
- If the song is PUBLIC DOMAIN, return FULL lyrics.
- If COPYRIGHTED, return lyric placeholders.
- Always return chords.
- Preserve sections exactly (Verse, Chorus, Refrain).

RETURN ONLY VALID JSON. NO MARKDOWN. NO TEXT.

JSON SCHEMA:
{{
  "title": "Song title",
  "artist": "Artist or composer",
  "public_domain": true,
  "sections": [
    {{
      "name": "Verse 1",
      "lines": [
        {{
          "chords": ["G", "G7", "C", "G"],
          "lyrics": "Amazing Grace, how sweet the sound"
        }}
      ]
    }}
  ]
}}

Song request: "{query}"
"""

    response = await client.responses.create(
        model=MODEL,
        input=prompt
    )

    raw = response.output_text.strip()

    try:
        return json.loads(raw)
    except Exception:
        return {
            "title": query,
            "artist": "Unknown",
            "public_domain": False,
            "sections": []
        }
