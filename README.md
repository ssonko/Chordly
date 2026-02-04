# Universal Chord → Number System Conversion

This project defines a system for converting any musical chord notation into number-based notation (Nashville Number System) relative to a given key, while preserving harmonic meaning, chord quality, extensions, alterations, inversions, and bass notes.

The system must work for all chord types, not only slash chords.

---

## Problem Summary

Create a conversion engine that:
- Accepts standard chord notation (e.g. `G7♭9/B`)
- Converts chord roots and bass notes into scale-degree numbers
- Preserves all chord qualities, extensions, and alterations verbatim
- Produces consistent, transposable Nashville-style output across all keys

---

## Core Principles

### Key-Relative Conversion
- All notes are interpreted relative to the active key
- The same chord maps to different numbers in different keys

### Chord Identity Comes From the Root
- The root note defines the chord number
- Everything else modifies or decorates that number

### Notation Preservation
- Chord quality and extensions are preserved exactly
- Only letter note names are replaced by scale degrees

---

## Supported Chord Components

The parser must recognize and preserve all of the following.

---

### 1. Basic Triads

| Type | Example | Output |
|----|-------|--------|
| Major | C | 1 |
| Minor | Am | 6m |
| Diminished | Bdim | 7dim |
| Augmented | Caug | 1aug |

---

### 2. Seventh Chords

| Type | Example | Output |
|----|-------|--------|
| Dominant 7 | G7 | 5⁷ |
| Major 7 | Cmaj7 | 1maj7 |
| Minor 7 | Am7 | 6m7 |
| Half-diminished | Bm7♭5 | 7m7♭5 |
| Fully diminished | Bdim7 | 7dim7 |

---

### 3. Extensions (9, 11, 13)

Extensions must be kept, not reinterpreted.

C9 → 1⁹  
Am11 → 6m11  
G13 → 5¹³  

---

### 4. Suspended Chords

| Example | Output |
|------|------|
| Csus2 | 1sus2 |
| Dsus4 | 2sus4 |
| G7sus4 | 5⁷sus4 |

---

### 5. Added-Tone Chords

| Example | Output |
|------|------|
| Cadd9 | 1add9 |
| Amadd11 | 6madd11 |

---

### 6. Altered Chords

Alterations remain intact.

| Example | Output |
|------|------|
| G7♭9 | 5⁷♭9 |
| C♯11 | 1♯11 |
| D7♯5 | 2⁷♯5 |

---

### 7. Slash Chords (Inversions & Pedal Bass)

Slash chords must be parsed into:
- Chord root
- Bass note

Each is converted independently.

Example (Key of C):

G/B   → 5/7  
G/C   → 5/1  
Am7/E → 6m7/3  

Format:
<number><quality>/<bass_number>

---

### 8. Accidentals

- Sharps (#) and flats (♭) must be supported
- Enharmonic equivalents should be normalized internally

Examples:

F# → ♯4 (in key of C)  
Bb → ♭7  

---

### 9. Roman Numeral Mode (Optional)

If enabled:
- Uppercase = major
- Lowercase = minor

Examples:

Am → vi  
C  → I  

(Default mode uses Arabic numerals.)

---

## Parsing Rules (Critical for Implementation)

1. Split slash chords  
   - If `/` exists, split into `chord_part` and `bass_note`

2. Extract chord root  
   - First pitch class, including accidental

3. Extract chord modifiers  
   - Everything after the root:
     - m, maj, dim, aug
     - numbers: 7, 9, 11, 13
     - modifiers: sus, add, ♭, ♯

4. Convert notes to scale degrees  
   - Use key-based scale mapping
   - Support chromatic offsets

5. Reassemble  
   - Replace root with number
   - Append modifiers unchanged
   - Append `/bass_number` if present

---

## Inputs and Outputs

Input:
{
  "key": "C",
  "chord": "G7♭9/B"
}

Output:
5⁷♭9/7

---

## Design Philosophy

- Numbers express harmonic function, not voicing
- Chord quality is never inferred or altered
- Bass notes affect voicing, not harmony
- The same progression must work identically in all keys

---

## Edge Cases to Handle

- Enharmonic equivalents (A# vs Bb)
- Chords outside the diatonic scale
- Borrowed chords
- Secondary dominants (V/V logic, optional)
- No-chord notation (N.C.)

---

## Intended Use

This specification is intended to:
- Be implemented directly in code (Python, JavaScript, etc.)
- Be used as a prompt or reference for LLM-based code generation
- Serve as a foundation for advanced harmonic analysis systems
