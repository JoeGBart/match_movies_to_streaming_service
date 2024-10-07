'''
Streaming services
'''

import requests
import json
import streamlit as st
from fuzzywuzzy import process
from streamlit_searchbox import st_searchbox

from streamlit_app.justwatch_queries import generate_service_search_query, url

def fetch_services(url):
    query = generate_service_search_query()
    response = requests.post(url, json=query)
    service_details = response.json()['data']['packages']
    print(
        json.dumps(
            service_details,
            indent=2,
        )
    )
    services = []
    accepted_monetization_types = ['FLATRATE','ADS','FREE']
    for service in service_details:
        if service['hasTitles'] and any(service in accepted_monetization_types for service in service['monetizationTypes']):
            services += [{'clearName':service['clearName'],'hasSport':service['hasSport'],'hasTitles':service['hasTitles'],'monetizationTypes':service['monetizationTypes'],'packageId':service['packageId']}]
            # services += [service]
    return services
    
def search_services(searchterm):
    all_services = fetch_services(url)
    all_service_names = [service['clearName'] for service in all_services]
    matches = process.extract(searchterm, all_service_names, limit=5) 
    
    return matches if searchterm else []
    
if __name__== '__main__':
    services = fetch_services(url)
    # st.write(services)
    st.header("Add Your Services", divider="green")

    selected_value = st_searchbox(
        search_services,
        key="service_searchbox",
    )

    # st.button("Reset", type="primary")
    if st.button("Add To Service List"):
        # movie_status = add_movie_to_file(movie_fpath, {'node_id':selected_value[0],'movie_title':selected_value[1]})
        st.write(f"**{selected_value} added to service list**")
        st.rerun()
        