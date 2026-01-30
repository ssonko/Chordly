import os
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def search_song(query: str):
    prompt = f"""Find the song requested and return chords and lyrics.
    Query: {query}
    Format response with chords above lyrics.
    """

    response = await client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "query": query,
        "result": response.choices[0].message.content
    }