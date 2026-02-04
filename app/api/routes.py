from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.openai_service import search_song
import json

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/features", response_class=HTMLResponse)
def features(request: Request):
    return templates.TemplateResponse("features.html", {"request": request})


@router.get("/pricing", response_class=HTMLResponse)
def pricing(request: Request):
    return templates.TemplateResponse("pricing.html", {"request": request})


@router.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@router.get("/search", response_class=HTMLResponse)
def search_page(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})


@router.get("/song_details", response_class=HTMLResponse)
def song_details(request: Request):
    song = request.session.get("song_data")

    if not song:
        return RedirectResponse("/search")

    return templates.TemplateResponse(
        "song_details.html",
        {
            "request": request,
            "song": song
        }
    )


@router.post("/api/search")
async def search_api(request: Request, payload: dict):
    query = payload.get("query")
    if not query:
        return JSONResponse({"error": "Missing query"}, status_code=400)

    result = await search_song(query)

    song_data = json.loads(result) if isinstance(result, str) else result

    # ✅ STEP 2: normalize here
    song_data = normalize_song(song_data)

    # ✅ STEP 3: store clean data only
    request.session["song_data"] = song_data

    return JSONResponse({"redirect": "/song_details"})


@router.get("/debug-session")
def debug_session(request: Request):
    return {
        "session_exists": "session" in request.scope,
        "session_data": request.session
    }

def normalize_song(song: dict) -> dict:
    """
    Guarantees:
    - One chord line per lyric line
    - No chord-only lines
    - No empty lyrics
    """

    for section in song.get("sections", []):
        normalized_lines = []
        chord_buffer = []

        for line in section.get("lines", []):
            chords = line.get("chords", [])
            lyrics = (line.get("lyrics") or "").strip()

            # Accumulate stray chord-only lines
            if chords and not lyrics:
                chord_buffer.extend(chords)
                continue

            # Valid lyric line → attach buffered chords
            if lyrics:
                normalized_lines.append({
                    "chords": chord_buffer + chords,
                    "lyrics": lyrics
                })
                chord_buffer = []

        section["lines"] = normalized_lines

    return song
