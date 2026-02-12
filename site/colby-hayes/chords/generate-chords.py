#!/usr/bin/env python3
"""Generate chord pages for all Colby Hayes songs"""

from pathlib import Path

SONGS = [
    {
        "slug": "midnight-thoughts",
        "title": "Midnight Thoughts",
        "track": 1,
        "key": "G Major",
        "capo": "2nd fret",
        "tempo": "76 BPM",
        "chords": ["G", "D", "Em", "C"],
        "progression_verse": "G - D - Em - C",
        "progression_chorus": "Em - C - G - D",
        "progression_bridge": "C - Em - D - G",
        "strumming": "D D U U D U",
        "notes": "Use fingerpicking on verses, switch to strumming on chorus. Let the G chord ring out during pauses."
    },
    {
        "slug": "paper-walls",
        "title": "Paper Walls",
        "track": 2,
        "key": "C Major",
        "capo": "No capo",
        "tempo": "82 BPM",
        "chords": ["C", "Am", "F", "G"],
        "progression_verse": "C - Am - F - G",
        "progression_chorus": "F - G - C - Am",
        "progression_bridge": "Am - F - C - G",
        "strumming": "D DU UDU",
        "notes": "Keep the rhythm light and bouncy. Emphasize the downbeats on the chorus."
    },
    {
        "slug": "exit-sign",
        "title": "Exit Sign",
        "track": 3,
        "key": "A Minor",
        "capo": "3rd fret",
        "tempo": "68 BPM",
        "chords": ["Am", "F", "C", "G"],
        "progression_verse": "Am - F - C - G",
        "progression_chorus": "F - C - G - Am",
        "progression_bridge": "Am - G - F - F",
        "strumming": "D D D DU",
        "notes": "Slow and deliberate. Let each chord breathe before transitioning."
    },
    {
        "slug": "somewhere-between",
        "title": "Somewhere Between",
        "track": 4,
        "key": "D Major",
        "capo": "2nd fret",
        "tempo": "88 BPM",
        "chords": ["D", "A", "Bm", "G"],
        "progression_verse": "D - A - Bm - G",
        "progression_chorus": "Bm - G - D - A",
        "progression_bridge": "G - D - A - Bm",
        "strumming": "D U D U D U",
        "notes": "Continuous eighth notes. Build intensity through repetition."
    },
    {
        "slug": "twenty-something",
        "title": "Twenty-Something",
        "track": 5,
        "key": "E Major",
        "capo": "No capo",
        "tempo": "96 BPM",
        "chords": ["E", "B", "C#m", "A"],
        "progression_verse": "E - B - C#m - A",
        "progression_chorus": "A - E - B - C#m",
        "progression_bridge": "C#m - A - E - B",
        "strumming": "D D UDU D U",
        "notes": "Upbeat anthem energy. Accent every other downbeat for punch."
    },
    {
        "slug": "almost-called",
        "title": "Almost Called",
        "track": 6,
        "key": "A Major",
        "capo": "2nd fret",
        "tempo": "72 BPM",
        "chords": ["A", "E", "F#m", "D"],
        "progression_verse": "A - E - F#m - D",
        "progression_chorus": "D - A - E - F#m",
        "progression_bridge": "F#m - D - A - E",
        "strumming": "D D D U D U",
        "notes": "Vulnerable and intimate. Keep volume low on verses, swell on chorus."
    },
    {
        "slug": "static",
        "title": "Static",
        "track": 7,
        "key": "E Minor",
        "capo": "4th fret",
        "tempo": "64 BPM",
        "chords": ["Em", "C", "G", "D"],
        "progression_verse": "Em - C - G - D",
        "progression_chorus": "C - G - D - Em",
        "progression_bridge": "G - D - Em - C",
        "strumming": "D D U D U U",
        "notes": "Darkest song on the album. Let notes decay before the next chord."
    },
    {
        "slug": "better-stranger",
        "title": "Better Stranger",
        "track": 8,
        "key": "G Major",
        "capo": "3rd fret",
        "tempo": "78 BPM",
        "chords": ["G", "Em", "C", "D"],
        "progression_verse": "G - Em - C - D",
        "progression_chorus": "C - D - G - Em",
        "progression_bridge": "Em - C - G - D",
        "strumming": "D DU D DU",
        "notes": "Bittersweet feel. Mix fingerpicking intro with strummed chorus."
    },
    {
        "slug": "hometown-ghost",
        "title": "Hometown Ghost",
        "track": 9,
        "key": "C Major",
        "capo": "No capo",
        "tempo": "84 BPM",
        "chords": ["C", "G", "Am", "F"],
        "progression_verse": "C - G - Am - F",
        "progression_chorus": "Am - F - C - G",
        "progression_bridge": "F - Am - G - C",
        "strumming": "D D D D U D",
        "notes": "Nostalgic and wistful. Think campfire singalong energy."
    },
    {
        "slug": "learn-to-leave",
        "title": "Learn to Leave",
        "track": 10,
        "key": "D Major",
        "capo": "5th fret",
        "tempo": "66 BPM",
        "chords": ["D", "G", "Bm", "A"],
        "progression_verse": "D - G - Bm - A",
        "progression_chorus": "Bm - A - D - G",
        "progression_bridge": "G - Bm - A - D",
        "strumming": "D D U D U",
        "notes": "Album closer. Start sparse, build to full strum by final chorus."
    },
]

TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} Chords - Colby Hayes | Static in the Dark</title>
    <meta name="description" content="Guitar chords and tabs for '{title}' by Colby Hayes. Key of {key}, {capo}. Learn to play this song from Static in the Dark.">
    <meta name="keywords" content="{title} chords, Colby Hayes guitar, {title} tabs, how to play {title}">
    <link rel="canonical" href="https://reclaimmedia.co/colby-hayes/chords/{slug}.html">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../styles.css">
    <style>
        .chord-box {{
            display: inline-block;
            background: rgba(77, 184, 201, 0.15);
            border: 1px solid var(--accent);
            border-radius: 6px;
            padding: 0.5rem 1rem;
            margin: 0.25rem;
            font-family: monospace;
            font-size: 1.1rem;
        }}
        .progression {{
            background: rgba(26, 58, 74, 0.6);
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
            font-family: monospace;
            font-size: 1.2rem;
            letter-spacing: 0.05em;
        }}
        .section-label {{
            font-size: 0.85rem;
            color: var(--gold);
            margin-bottom: 0.5rem;
            font-weight: 600;
        }}
        .strumming-pattern {{
            font-size: 1.5rem;
            letter-spacing: 0.3em;
            color: var(--accent);
        }}
    </style>
</head>
<body>
    <nav class="nav">
        <div class="nav-inner">
            <a href="../index.html" class="nav-brand">Colby Hayes</a>
            <div class="nav-links">
                <a href="../">Home</a>
                <a href="../lyrics/">Lyrics</a>
                <a href="./">Chords</a>
                <a href="../meaning/">Song Meanings</a>
                <a href="../playlists/">Playlists</a>
            </div>
        </div>
    </nav>

    <div class="container">
        <div class="breadcrumb">
            <a href="../">Colby Hayes</a>
            <span>›</span>
            <a href="./">Chords</a>
            <span>›</span>
            {title}
        </div>

        <header class="page-header">
            <h1>{title}</h1>
            <p class="subtitle">Guitar Chords & Tabs</p>
        </header>

        <div class="content-card">
            <div class="song-info">
                <div class="song-info-item">
                    <div class="label">Key</div>
                    <div class="value">{key}</div>
                </div>
                <div class="song-info-item">
                    <div class="label">Capo</div>
                    <div class="value">{capo}</div>
                </div>
                <div class="song-info-item">
                    <div class="label">Tempo</div>
                    <div class="value">{tempo}</div>
                </div>
                <div class="song-info-item">
                    <div class="label">Track</div>
                    <div class="value">{track}</div>
                </div>
            </div>
        </div>

        <div class="content-card">
            <h2>Chords Used</h2>
            <div class="chords-used">
                {chord_boxes}
            </div>
        </div>

        <div class="content-card">
            <h2>Chord Progressions</h2>
            
            <div class="section-label">VERSE</div>
            <div class="progression">{progression_verse}</div>
            
            <div class="section-label">CHORUS</div>
            <div class="progression">{progression_chorus}</div>
            
            <div class="section-label">BRIDGE</div>
            <div class="progression">{progression_bridge}</div>
        </div>

        <div class="content-card">
            <h2>Strumming Pattern</h2>
            <p class="strumming-pattern">{strumming}</p>
            <p style="margin-top: 1rem; color: var(--slate);">D = Down, U = Up</p>
        </div>

        <div class="content-card">
            <h2>Playing Tips</h2>
            <p>{notes}</p>
        </div>

        <div class="nav-links-bottom">
            <a href="../lyrics/{slug}.html" class="btn">View Lyrics →</a>
            <a href="../meaning/{slug}.html" class="btn btn-secondary">Song Meaning →</a>
        </div>
    </div>

    <footer class="footer">
        <div class="footer-content">
            <p>&copy; 2026 Colby Hayes. All rights reserved.</p>
            <p>Chords are interpretations for educational purposes.</p>
        </div>
    </footer>
</body>
</html>'''

def main():
    output_dir = Path(__file__).parent
    
    for song in SONGS:
        chord_boxes = "\n                ".join(
            f'<span class="chord-box">{chord}</span>' for chord in song["chords"]
        )
        
        html = TEMPLATE.format(
            title=song["title"],
            slug=song["slug"],
            track=song["track"],
            key=song["key"],
            capo=song["capo"],
            tempo=song["tempo"],
            chord_boxes=chord_boxes,
            progression_verse=song["progression_verse"],
            progression_chorus=song["progression_chorus"],
            progression_bridge=song["progression_bridge"],
            strumming=song["strumming"],
            notes=song["notes"],
        )
        
        output_path = output_dir / f"{song['slug']}.html"
        output_path.write_text(html)
        print(f"✓ Created {song['slug']}.html")
    
    print(f"\nGenerated {len(SONGS)} chord pages")

if __name__ == "__main__":
    main()
