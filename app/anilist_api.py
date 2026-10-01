import requests

ANIList_API_URL = "https://graphql.anilist.co"

def search_anime(query, page=1, is_adult=False):
    graphql_query = """
    query ($search: String, $page: Int, $isAdult: Boolean) {
        Page(page: $page, perPage: 20) {
            media(search: $search, type: ANIME, isAdult: $isAdult) {
                id
                title { romaji english native }
                coverImage { large color }
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
    variables = {'search': query, 'page': page, 'isAdult': is_adult}
    response = requests.post(ANIList_API_URL, json={'query': graphql_query, 'variables': variables})
    if response.status_code == 200:
        return response.json()['data']['Page']['media']
    return []

def get_popular_anime(page=1, per_page=24, is_adult=False):
    graphql_query = """
    query ($page: Int, $perPage: Int, $isAdult: Boolean) {
        Page(page: $page, perPage: $perPage) {
            media(type: ANIME, sort: POPULARITY_DESC, isAdult: $isAdult) {
                id
                title { romaji english native }
                coverImage { large color }
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
    variables = {'page': page, 'perPage': per_page, 'isAdult': is_adult}
    response = requests.post(ANIList_API_URL, json={'query': graphql_query, 'variables': variables})
    if response.status_code == 200:
        return response.json()['data']['Page']['media']
    return []

def get_trending_anime(page=1, per_page=24, is_adult=False):
    graphql_query = """
    query ($page: Int, $perPage: Int, $isAdult: Boolean) {
        Page(page: $page, perPage: $perPage) {
            media(type: ANIME, sort: TRENDING_DESC, isAdult: $isAdult) {
                id
                title { romaji english native }
                coverImage { large color }
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
    variables = {'page': page, 'perPage': per_page, 'isAdult': is_adult}
    response = requests.post(ANIList_API_URL, json={'query': graphql_query, 'variables': variables})
    if response.status_code == 200:
        return response.json()['data']['Page']['media']
    return []

def get_popular_manga(page=1, per_page=24, is_adult=False):
    graphql_query = """
    query ($page: Int, $perPage: Int, $isAdult: Boolean) {
        Page(page: $page, perPage: $perPage) {
            media(type: MANGA, sort: POPULARITY_DESC, isAdult: $isAdult) {
                id
                title { romaji english native }
                coverImage { large color }
                bannerImage
                format
                status
                chapters
                averageScore
                genres
                description
            }
        }
    }
    """
    variables = {'page': page, 'perPage': per_page, 'isAdult': is_adult}
    response = requests.post(ANIList_API_URL, json={'query': graphql_query, 'variables': variables})
    if response.status_code == 200:
        return response.json()['data']['Page']['media']
    return []

def get_trending_manga(page=1, per_page=24, is_adult=False):
    graphql_query = """
    query ($page: Int, $perPage: Int, $isAdult: Boolean) {
        Page(page: $page, perPage: $perPage) {
            media(type: MANGA, sort: TRENDING_DESC, isAdult: $isAdult) {
                id
                title { romaji english native }
                coverImage { large color }
                bannerImage
                format
                status
                chapters
                averageScore
                genres
                description
            }
        }
    }
    """
    variables = {'page': page, 'perPage': per_page, 'isAdult': is_adult}
    response = requests.post(ANIList_API_URL, json={'query': graphql_query, 'variables': variables})
    if response.status_code == 200:
        return response.json()['data']['Page']['media']
    return []

def get_anime_by_id(anime_id):
    graphql_query = """
    query ($id: Int) {
        Media(id: $id, type: ANIME) {
            id
            title { romaji english native }
            coverImage { extraLarge large color }
            bannerImage
            format
            status
            episodes
            duration
            averageScore
            popularity
            genres
            description
            studios { nodes { name } }
            seasons
            seasonYear
        }
    }
    """
    response = requests.post(ANIList_API_URL, json={'query': graphql_query, 'variables': {'id': anime_id}})
    if response.status_code == 200:
        return response.json()['data']['Media']
    return None