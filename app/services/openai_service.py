import re
from collections import Counter

# =========================
# CONFIG
# =========================

CHORD_REGEX = r"\b([A-G](#|b)?(maj7|m7|m|sus2|sus4|dim|aug|add9|7)?)\b"

# =========================
# PARSE USER-PASTED CHART
# =========================

def parse_user_chart(title: str, artist: str, pasted_text: str) -> dict:
    lines = pasted_text.splitlines()
    sections = []
    current_section = {"name": "Song", "lines": []}

    i = 0
    while i < len(lines):
        raw_line = lines[i]
        line = raw_line.strip()

        # SECTION DETECTION
        if line.startswith("[") and line.endswith("]"):
            if current_section["lines"]:
                sections.append(current_section)
            current_section = {"name": line.strip("[]"), "lines": []}
            i += 1
            continue

        # CHORD LINE DETECTION
        chords = re.findall(CHORD_REGEX, line)

        if chords:
            chord_list = [c[0] for c in chords]

            lyric_line = ""
            if i + 1 < len(lines):
                lyric_line = lines[i + 1].strip()

            current_section["lines"].append({
                "chords": chord_list,
                "lyrics": lyric_line
            })

            i += 2
        else:
            i += 1

    if current_section["lines"]:
        sections.append(current_section)

    return {
        "title": title,
        "artist": artist,
        "sections": sections
    }

# =========================
# DETECT LIKELY KEY
# =========================

def detect_key(song: dict) -> str:
    chord_counter = Counter()

    for section in song["sections"]:
        for line in section["lines"]:
            for chord in line["chords"]:
                base = re.match(r"[A-G](#|b)?", chord)
                if base:
                    chord_counter[base.group()] += 1

    if not chord_counter:
        return "G"

    return chord_counter.most_common(1)[0][0]

# =========================
# TRANSPOSE ENGINE
# =========================

CHROMATIC = [
    "C","C#","D","D#","E","F","F#",
    "G","G#","A","A#","B"
]

def transpose_chord(chord: str, semitones: int) -> str:
    match = re.match(r"([A-G](#|b)?)(.*)", chord)
    if not match:
        return chord

    root = match.group(1)
    suffix = match.group(3)

    if root not in CHROMATIC:
        return chord

    new_index = (CHROMATIC.index(root) + semitones) % 12
    return CHROMATIC[new_index] + suffix


def transpose_song(song: dict, from_key: str, to_key: str) -> dict:
    if from_key not in CHROMATIC or to_key not in CHROMATIC:
        return song

    semitones = CHROMATIC.index(to_key) - CHROMATIC.index(from_key)

    for section in song["sections"]:
        for line in section["lines"]:
            line["chords"] = [
                transpose_chord(ch, semitones) for ch in line["chords"]
            ]

    return song

# =========================
# NASHVILLE NUMBER CONVERTER
# =========================

MAJOR_SCALES = {
    "C": ["C","Dm","Em","F","G","Am","Bdim"],
    "G": ["G","Am","Bm","C","D","Em","F#dim"],
    "D": ["D","Em","F#m","G","A","Bm","C#dim"],
    "A": ["A","Bm","C#m","D","E","F#m","G#dim"],
    "E": ["E","F#m","G#m","A","B","C#m","D#dim"]
}

def convert_to_numbers(song: dict, key: str) -> dict:
    scale = MAJOR_SCALES.get(key)
    if not scale:
        return song

    mapping = {scale[i]: str(i+1) for i in range(len(scale))}

    for section in song["sections"]:
        for line in section["lines"]:
            converted = []
            for chord in line["chords"]:
                base = re.match(r"[A-G](#|b)?m?", chord)
                if base and base.group() in mapping:
                    num = mapping[base.group()]
                    if "m" in chord and not base.group().endswith("m"):
                        num += "m"
                    converted.append(num)
                else:
                    converted.append(chord)
            line["chords"] = converted

    return song

# =========================
# PRINT FOR DEBUG
# =========================

def print_song(song: dict):
    print(f"\n🎵 {song['title']} — {song['artist']}\n")
    for section in song["sections"]:
        print(f"[{section['name']}]")
        for line in section["lines"]:
            print(" ".join(line["chords"]))
            print(line["lyrics"])
        print()