from agents import movie_agent
from data_models import Genre, Movie
from fastapi import FastAPI
from setup_db import query_duckdb

app = FastAPI()


# genre is optional -> /movies returns all, /movies?genre=action filters
@app.get("/movies")
async def read_movies(genre: Genre | None = None) -> list[Movie]:
    if genre:
        df = query_duckdb("SELECT * FROM movies WHERE genre = ?", parameters=[genre])
    else:
        df = query_duckdb("SELECT * FROM movies")

    return df.to_dict(orient="records")


@app.post("/movie")
async def create_movie(query: str) -> Movie:
    result = await movie_agent.run(query)
    movie = result.output

    query_duckdb(
        "INSERT INTO movies VALUES (?,?,?,?,?)",
        parameters=[movie.title, movie.year, movie.genre, movie.rating, movie.summary],
    )

    return movie
