import streamlit as st
import pandas as pd
import pickle
import requests
import gzip

# Fetch the movie poster from TMDB API
def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=7dc58daff23a79e45d57491f93a02fef")
    data = response.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Recommend similar movies
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # Fetching posters of recommended movies
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Load movie data
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

# Decompress and load the similarity data
with gzip.open("similarity.pkl.gz", "rb") as f:
    similarity = pickle.load(f)

# Title of the app
st.markdown(
    """
    <h1 style='text-align: center; color: #E05123;'>🎬 Movie Recommender System</h1>
    """,
    unsafe_allow_html=True
)

# Subtitle for movie selection
st.markdown(
    """
    <h2 style='text-align: left; color: #B75151;'>🍿 Select a movie 📽️:</h2>
    """,
    unsafe_allow_html=True
)

# Dropdown to select a movie
selected_movie_name = st.selectbox(
    '',
    movies["title"].values
)

# Display the selected movie name
if selected_movie_name:
    st.markdown(f"<h3 style='color: #ABB1B1; text-align: center;'>{selected_movie_name}</h3>", unsafe_allow_html=True)

# Recommend button functionality
if st.button("Recommend 🔍"):
    names, posters = recommend(selected_movie_name)

    # Display recommended movies and posters
    columns = st.columns(5)
    for i, col in enumerate(columns):
        with col:
            st.text(names[i])
            st.image(posters[i], use_column_width=True)