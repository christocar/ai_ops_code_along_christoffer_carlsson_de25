import httpx
import pandas as pd
import streamlit as st
from data_models import GENRES

API_URL = "http://127.0.0.1:8000"

st.title("Movie finder")

# ask a question -> POST /movie -> agent finds movie and api saves it to db
query = st.text_input("Describe a movie or write a famous quote")

if st.button("Find and save movie") and query:
    with st.spinner("Asking the agent..."):
        # llm calls can be slow, default timeout of 5s is too short
        response = httpx.post(f"{API_URL}/movie", params={"query": query}, timeout=60)

    if response.status_code == 200:
        movie = response.json()
        st.success(f"Saved: {movie['title']} ({movie['year']})")
        st.json(movie)
    else:
        st.error(f"Something went wrong: {response.text}")

# filter on genre -> GET /movies?genre=...
st.header("Saved movies")
genre = st.selectbox("Filter on genre", ["all"] + GENRES)

params = {} if genre == "all" else {"genre": genre}
movies = httpx.get(f"{API_URL}/movies", params=params).json()

st.dataframe(pd.DataFrame(movies), hide_index=True)
