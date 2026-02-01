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
    prompt = f"""Find the song requested and return chords and lyrics.
    Query: {query}
    Format response with chords above lyrics.
    """

    response = await client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5-nano"),
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "query": query,
        "result": response.choices[0].message.content
    }
