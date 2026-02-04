import os
import json
from dotenv import load_dotenv
from openai import AsyncOpenAI

# Load .env from project root
load_dotenv(
    dotenv_path=os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../.env")
    ),
    override=True
)

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-5-nano")


async def search_song(query: str) -> dict:
    """
    Returns structured song data safe for rendering.
    NO hard-coded values.
    NO copyrighted lyrics beyond short excerpts.
    """

    prompt = f"""
You are a music assistant.

Return ONLY valid JSON.
Do NOT include markdown.
Do NOT include explanations.

Task:
- Identify the requested song
- Provide guitar chords aligned above lyric placeholders
- Do NOT return full copyrighted lyrics
- Use short lyric fragments or placeholders

JSON FORMAT (must match exactly):

{{
  "title": "Song Title",
  "artist": "Artist Name",
  "key": "C Major",
  "time_signature": "4/4",
  "sections": [
    {{
      "name": "Verse 1",
      "lines": [
        {{
          "chords": ["C", "G", "Am"],
          "lyrics": "(lyrics omitted)"
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

    raw_text = response.output_text.strip()

    try:
        song_data = json.loads(raw_text)
    except json.JSONDecodeError:
        # Hard fallback so UI never crashes
        song_data = {
            "title": query,
            "artist": "Unknown Artist",
            "key": "Unknown",
            "time_signature": "Unknown",
            "sections": []
        }

    return song_data
