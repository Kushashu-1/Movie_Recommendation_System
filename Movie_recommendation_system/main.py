import streamlit as st
import pickle
import pandas as pd
import requests

similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    # Using Campus-X TMDB API Key
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=0cc7e32beda738dbefc3c6cd2f6a3b4e&language=en-US")
    data = response.json()
    poster_path = data['poster_path']
    return "https://image.tmdb.org/t/p/w500/" + poster_path


def recommender(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),
                         reverse=True, key=lambda x: x[1])
    recommended_movies = []
    m_poster = []
    for i in movies_list[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        m_poster.append(fetch_poster(movie_id))
    return recommended_movies, m_poster

st.title("Movie Recommendation System")

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

selected = st.selectbox("Select Movie Name", movies['title'].values)
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommender(selected)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
