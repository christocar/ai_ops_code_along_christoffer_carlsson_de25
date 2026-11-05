import httpx

API_URL = "http://127.0.0.1:8000"

# one query per movie -> try to cover all genres
queries = [
    "May the Force be with you",
    "I'm the king of the world!",
    "To infinity and beyond!",
    "Why so serious?",
    "Here's looking at you, kid",
    "Hakuna Matata",
    "You're gonna need a bigger boat",
    "Yippee-ki-yay",
    "Life is like a box of chocolates",
    "I'll have what she's having",
    "Just keep swimming",
    "Fortune and glory, kid. Fortune and glory",
    "Wax on, wax off",
    "Nobody puts Baby in a corner",
    "Groovy, baby!",
]

# api must be running: uv run uvicorn api:app --reload
for query in queries:
    try:
        response = httpx.post(f"{API_URL}/movie", params={"query": query}, timeout=90)
        response.raise_for_status()
        movie = response.json()
        print(f"saved: {movie['title']} ({movie['year']}) - {movie['genre']}")
    except httpx.HTTPError as error:
        # one failing llm call shouldn't stop the rest
        print(f"failed: {query} -> {error}")
