import requests

ANIList_API_URL = "https://graphql.anilist.co"

def search_anime(query, page=1):
    graphql_query = """
    query ($search: String, $page: Int) {
        Page(page: $page, perPage: 20) {
            media(search: $search, type: ANIME) {
                id
                title {
                    romaji
                    english
                    native
                }
                coverImage {
                    large
                    color
                }
                bannerImage
                format
                status
                episodes
                averageScore
                genres
                description
            }
        }
    }
    """
    
    variables = {'search': query, 'page': page}
    response = requests.post(
        ANIList_API_URL,
        json={'query': graphql_query, 'variables': variables}
    )
    
    if response.status_code == 200:
        data = response.json()
        return data['data']['Page']['media']
    return []

def get_popular_anime(page=1):
    graphql_query = """
    query ($page: Int) {
        Page(page: $page, perPage: 12) {
            media(type: ANIME, sort: POPULARITY_DESC) {
                id
                title {
                    romaji
                    english
                    native
                }
                coverImage {
                    large
                    color
                }
                bannerImage
                format
                status
                episodes
                averageScore
                genres
                description
            }
        }
    }
    """
    
    variables = {'page': page}
    response = requests.post(
        ANIList_API_URL,
        json={'query': graphql_query, 'variables': variables}
    )
    
    if response.status_code == 200:
        data = response.json()
        return data['data']['Page']['media']
    return []

def get_trending_anime(page=1):
    graphql_query = """
    query ($page: Int) {
        Page(page: $page, perPage: 12) {
            media(type: ANIME, sort: TRENDING_DESC) {
                id
                title {
                    romaji
                    english
                    native
                }
                coverImage {
                    large
                    color
                }
                bannerImage
                format
                status
                episodes
                averageScore
                genres
                description
            }
        }
    }
    """
    
    variables = {'page': page}
    response = requests.post(
        ANIList_API_URL,
        json={'query': graphql_query, 'variables': variables}
    )
    
    if response.status_code == 200:
        data = response.json()
        return data['data']['Page']['media']
    return []

def get_anime_by_id(anime_id):
    graphql_query = """
    query ($id: Int) {
        Media(id: $id, type: ANIME) {
            id
            title {
                romaji
                english
                native
            }
            coverImage {
                extraLarge
                large
                color
            }
            bannerImage
            format
            status
            episodes
            duration
            averageScore
            popularity
            genres
            description
            studios {
                nodes {
                    name
                }
            }
            seasons
            seasonYear
        }
    }
    """
    
    response = requests.post(
        ANIList_API_URL,
        json={'query': graphql_query, 'variables': {'id': anime_id}}
    )
    
    if response.status_code == 200:
        data = response.json()
        return data['data']['Media']
    return None