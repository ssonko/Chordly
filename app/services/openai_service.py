import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv(
    dotenv_path=os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../.env")
    ),
    override=True
)

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def search_song(query: str):
    prompt = f"""
SYSTEM ROLE:
You are a strict music chart extraction engine.
Your output will be parsed by software.
Formatting errors will cause the application to fail.

ABSOLUTE OUTPUT RULES (MANDATORY):
- Output ONLY valid JSON
- NO markdown
- NO commentary
- NO plain text
- NO blank lines
- NO extra keys
- NO chord-only lines
- NO lyric-only objects
- NEVER output chords on their own line

DATA MODEL RULE:
Each lyric line MUST be represented as an object with:
- "chords": array of chord symbols
- "lyrics": string

CHORD GROUPING RULE:
- Chords that appear ABOVE a lyric line belong to THAT lyric line
- Ignore visual spacing and alignment completely
- Preserve chord order exactly as it occurs in the song
- If a lyric line has no new chord changes, repeat the previous chord(s)

SECTION RULES:
- Detect and group sections (Verse, Chorus, Refrain, Bridge, Intro, Outro)
- Normalize labels (e.g. "Refrain" not "REFRAIN")
- If no section label exists, infer one

CHORD RULES:
- Use standard chord symbols only (C, G, Am, G7, F#, Bb, etc.)
- Do NOT align chords to syllables
- Do NOT attempt timing or rhythm
- Chords must be tokenized individually (no spacing artifacts)

LYRIC RULES:
- Preserve original lyric text exactly
- Do NOT invent lyrics
- Do NOT merge lyric lines
- Do NOT split lyric lines

REQUIRED OUTPUT SCHEMA:
{{
  "title": string,
  "artist": string,
  "key": string,
  "time_signature": string,
  "sections": [
    {{
      "label": string,
      "lines": [
        {{
          "chords": [string],
          "lyrics": string
        }}
      ]
    }}
  ]
}}
Repeat chord and lyrics for the entire song.

SONG REQUEST:
{query}
"""

    response = await client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5-nano"),
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.content
