'''
Just Watch base URLs and graphql queries
'''

url = "https://apis.justwatch.com/graphql"

def generate_title_search_query(searchterm: str, maxhits: int=5) -> dict:
    ''' Function generates a graphql query for the justwatch api that
        searches for Film titles that match the search term
        
        Args:
            searchterm: term to be searched
            maxhits: maximum number of hits to be returned from query
        returns:
            graphql query dictionary
    '''
    query = {
    "operationName": "GetSuggestedTitles",
    "variables": {
        "country": "GB",
        "language": "en",
        "first": maxhits,
        "filter": {"searchQuery": searchterm},
    },
    "query": "query GetSuggestedTitles($country: Country!, $language: Language!, $first: Int!, $filter: TitleFilter) {\n  popularTitles(country: $country, first: $first, filter: $filter) {\n    edges {\n      node {\n        ...SuggestedTitle\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment SuggestedTitle on MovieOrShow {\n  id\n  objectType\n  objectId\n  content(country: $country, language: $language) {\n    fullPath\n    title\n    originalReleaseYear\n    posterUrl\n    fullPath\n    __typename\n  }\n  watchNowOffer(country: $country, platform: WEB) {\n    id\n    standardWebURL\n    package {\n      id\n      packageId\n      __typename\n    }\n    __typename\n  }\n  offers(country: $country, platform: WEB) {\n    monetizationType\n    presentationType\n    standardWebURL\n    package {\n      id\n      packageId\n      __typename\n    }\n    id\n    __typename\n  }\n  __typename\n}\n",
    }
    return query
    
def generate_service_search_query() -> dict:
    ''' Function generates a graphql query for the justwatch api that
        searches for Streaming Services that match the search term
        
        Args:
            searchterm: term to be searched
            maxhits: maximum number of hits to be returned from query
        returns:
            graphql query dictionary
    '''
    query = {
    "query": "query GetPackages($country: Country!, $platform: Platform! = WEB) {\n\t\t\tpackages(country: $country, platform: $platform, includeAddons: true) {\n\t\t\t\tclearName\n\t\t\t\thasSport(country: $country, platform: $platform)\n\t\t\t\thasTitles(country: $country, platform: $platform)\n\t\t\t\ticon\n\t\t\t\tmonetizationTypes\n\t\t\t\tpackageId\n\t\t\t\tselected\n\t\t\t\tshortName\n\t\t\t\tslug\n\t\t\t\ttechnicalName\n\t\t\t}\n\t\t}",
    "variables": {
    "country": "GB",
    }}
    return query
    
def generate_movie_service_match(nodeid: str) -> dict: 
    ''' Function generates a graphql query for the justwatch api that
        searches for Streaming Services offerings for a particular movie title
        
        Args:
            nodeid: id of film to find service offerings
        returns:
            graphql query dictionary
    '''
    query = {
      "operationName": "GetTitleOffers",
      "variables": {
        "platform": "WEB",
        "nodeId": "tm11948",
        "country": "GB",
        "language": "en",
        "filterBuy": {
          "monetizationTypes": ["FLATRATE", "ADS", "FREE"],
          "bestOnly": True
        },
        "filterFlatrate": {
          "monetizationTypes": ["FLATRATE", "ADS", "FREE"],
          "bestOnly": True
        },
        "filterRent": {
          "monetizationTypes": ["FLATRATE", "ADS", "FREE"],
          "bestOnly": True
        },
        "filterFree": {
          "monetizationTypes": ["FLATRATE", "ADS", "FREE"],
          "bestOnly": True
        }
      },
      "query": "query GetTitleOffers($nodeId: ID!, $country: Country!, $language: Language!, $filterFlatrate: OfferFilter!, $filterBuy: OfferFilter!, $filterRent: OfferFilter!, $filterFree: OfferFilter!, $platform: Platform! = WEB) {\n  node(id: $nodeId) {\n    id\n    __typename\n    ... on MovieOrShowOrSeasonOrEpisode {\n      offerCount(country: $country, platform: $platform)\n      maxOfferUpdatedAt(country: $country, platform: $platform)\n      flatrate: offers(\n        country: $country\n        platform: $platform\n        filter: $filterFlatrate\n      ) {\n        ...TitleOffer\n        __typename\n      }\n      buy: offers(country: $country, platform: $platform, filter: $filterBuy) {\n        ...TitleOffer\n        __typename\n      }\n      rent: offers(country: $country, platform: $platform, filter: $filterRent) {\n        ...TitleOffer\n        __typename\n      }\n      free: offers(country: $country, platform: $platform, filter: $filterFree) {\n        ...TitleOffer\n        __typename\n      }\n      fast: offers(\n        country: $country\n        platform: $platform\n        filter: {monetizationTypes: [FAST], bestOnly: true}\n      ) {\n        ...FastOffer\n        __typename\n      }\n      __typename\n    }\n  }\n}\n\nfragment TitleOffer on Offer {\n  id\n  presentationType\n  monetizationType\n  retailPrice(language: $language)\n  retailPriceValue\n  currency\n  lastChangeRetailPriceValue\n  type\n  package {\n    id\n    packageId\n    clearName\n    technicalName\n    icon(profile: S100)\n    __typename\n  }\n  standardWebURL\n  elementCount\n  availableTo\n  deeplinkRoku: deeplinkURL(platform: ROKU_OS)\n  __typename\n}\n\nfragment FastOffer on Offer {\n  ...TitleOffer\n  availableTo\n  availableFromTime\n  availableToTime\n  __typename\n}\n"
    }
    return query