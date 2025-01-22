import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster
def poster_fetcher(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=57f88c1a1943f0c140138e8d0db192a7')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Function to recommend movies based on similarity
def content_recommend(movie):
    idx = movies[movies['title'] == movie].index[0]
    distance = similarity[idx]
    Movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in Movie_list:
        if i[0] < len(movies):
            Movie_id = movies.iloc[i[0]].id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_poster.append(poster_fetcher(Movie_id))
        else:
            st.error(f"Index {i[0]} is out of bounds for movies DataFrame.")

    return recommended_movies, recommended_movies_poster

# Load data
movie_dict = pickle.load(open('data_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('temp_similarity.pkl', 'rb'))

# Set page configuration
st.set_page_config(page_title="Movie Recommender System", layout="wide")

# Add a background image
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQkATan6TmhL7FOhQtzlIyKhFm3MUb-xM7kbQ&s");
        background-size: cover;
        background-position: center;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title of the app
st.title('🎬 Movie Recommender System 🎬')

# Movie selection dropdown
Selected_Movie_Name = st.selectbox(
    "Select a movie to get recommendations:",
    movies['title'].values
)

# Recommend button
if st.button("Recommend"):
    names, posters = content_recommend(Selected_Movie_Name)
    columns = st.columns(len(names))

    for j in range(len(names)):
        with columns[j]:
            st.image(posters[j], use_column_width=True)
            st.text(names[j])

# Footer
st.markdown(
    """
    <style>
    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("Made with ❤️ by Your Naman")