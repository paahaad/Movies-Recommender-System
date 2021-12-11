import streamlit as st
import pickle
import pandas as pd
import requests


similarity = pickle.load(open('similarity.pkl','rb'))
movies_list = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movies_list)

st.set_page_config(
     page_title="Parvat's-Project",
     page_icon="🦈",
     layout="centered",
     initial_sidebar_state="collapsed"
 )

st.title('Movie Recommender System')
option = st.selectbox(
     'Select movie you would to connect',
     (movies['title'].values))


def fetch_poster(movies_id):
    '''fetch poster from API'''
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movies_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


@st.cache()
def Recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key= lambda x:x[1])
    recommended_movies= []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies,recommended_movie_posters


if st.button('Recommend'):
    recommended_movie_names,recommended_movie_posters = Recommend(option)
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