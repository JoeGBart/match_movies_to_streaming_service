"""
Movies

Page to add and remove movies from movie list.
"""

import logging
import json
import streamlit as st
import requests
import json
import pandas as pd
import logging
from streamlit_searchbox import st_searchbox


def read_movies_from_file(movie_fpath: str) -> dict:
    try:
        movie_data = pd.read_csv(movie_fpath)
        num_movies = movie_data.shape[0]
        if num_movies == 0:
            return None
        else:
            return movie_data
    except FileNotFoundError:
        logging.info('No existing movie file.')
        return None


def search_film_justwatch(searchterm: str):
    url = "https://apis.justwatch.com/graphql"
    query = {
    "operationName": "GetSuggestedTitles",
    "variables": {
        "country": "GB",
        "language": "en",
        "first": 5,
        "filter": {"searchQuery": searchterm},
    },
    "query": "query GetSuggestedTitles($country: Country!, $language: Language!, $first: Int!, $filter: TitleFilter) {\n  popularTitles(country: $country, first: $first, filter: $filter) {\n    edges {\n      node {\n        ...SuggestedTitle\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment SuggestedTitle on MovieOrShow {\n  id\n  objectType\n  objectId\n  content(country: $country, language: $language) {\n    fullPath\n    title\n    originalReleaseYear\n    posterUrl\n    fullPath\n    __typename\n  }\n  watchNowOffer(country: $country, platform: WEB) {\n    id\n    standardWebURL\n    package {\n      id\n      packageId\n      __typename\n    }\n    __typename\n  }\n  offers(country: $country, platform: WEB) {\n    monetizationType\n    presentationType\n    standardWebURL\n    package {\n      id\n      packageId\n      __typename\n    }\n    id\n    __typename\n  }\n  __typename\n}\n",
    }
    print(searchterm)
    print('getting response')
    response = requests.post(url, json=query)
    title_details = response.json()["data"]["popularTitles"]["edges"]
    print(title_details)
    titles = []
    for title in title_details:
        # titles[title["node"]["content"]["title"]] = title["node"]["id"]
        titles += [(title["node"]["content"]["title"], (title["node"]["id"], title["node"]["content"]["title"],))]
        # print(title["node"]["id"])
        # print(title["node"]["objectType"])
        # print(title["node"]["content"]["title"])
        # print("\n\n")
    print(titles)
    return titles if searchterm else []


def add_movie_to_file(movie_fpath: str, movie):
    new_movie = pd.DataFrame(movie, index=[0])
    try:
        movie_data = pd.read_csv(movie_fpath)
        print(movie_data['node_id'])
        print(movie_data['node_id'].values)
        if movie['node_id'] in movie_data['node_id'].values:
            return 'already present in your movie list'
        else:
            movie_data = pd.concat([movie_data, new_movie])
            movie_data.to_csv(movie_fpath, index=False)
            return 'added to movie list'
    except FileNotFoundError:
        logging.info('No existing movie file.')
        new_movie.to_csv(movie_fpath, index=False)
        return 'added to movie list'
    


def remove_movie_from_file(movie_data, movie_title, movie_fpath):
    updated_movie_data = movie_data.drop(movie_data[movie_data['movie_title']==movie_title].index)
    updated_movie_data.to_csv(movie_fpath, index=False)
    return


if __name__ == "__main__":
    st.header("Your Movie List", divider="green")
    movie_fpath = "movies.csv"
    movie_data = read_movies_from_file(movie_fpath)
    if movie_data is None:
        st.write("**:grey_exclamation: No movies in list. Add movies below.**")
    else:
        movie_to_remove = st.radio("select to remove:", movie_data['movie_title'])
        if st.button("Remove From Movie List"):
            remove_movie_from_file(movie_data, movie_to_remove, movie_fpath)
            st.write(f"**{movie_to_remove} removed from movie list**")
            st.rerun()
            
    st.header("Add New Movies", divider="green")

    selected_value = st_searchbox(
        search_film_justwatch,
        key="movie_searchbox",
    )

    # st.button("Reset", type="primary")
    if st.button("Add To Movie List"):
        movie_status = add_movie_to_file(movie_fpath, {'node_id':selected_value[0],'movie_title':selected_value[1]})
        st.write(f"**{selected_value[1]} {movie_status}**")
        st.experimental_rerun()
        
        
