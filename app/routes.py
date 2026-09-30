from flask import Blueprint, render_template, request, session, jsonify
from app.anilist_api import (
    search_anime,
    get_anime_by_id,
    get_popular_anime,
    get_trending_anime,
    get_popular_manga,
    get_trending_manga,
)
from app.translit import translit

bp = Blueprint('main', __name__)

@bp.route('/set_language/<lang>')
def set_language(lang):
    if lang in ['en', 'ru']:
        session['language'] = lang
    return jsonify({'success': True})

@bp.route('/')
def index():
    is_adult = session.get('show_adult', False)
    popular = get_popular_anime(is_adult=is_adult)
    trending = get_trending_anime(is_adult=is_adult)
    popular_manga = get_popular_manga(is_adult=is_adult)
    trending_manga = get_trending_manga(is_adult=is_adult)
    featured = trending[:10] if trending else []
    return render_template('index.html',
                           popular=popular, trending=trending,
                           popular_manga=popular_manga, trending_manga=trending_manga,
                           featured=featured)

@bp.route('/search')
def search_page():
    query = request.args.get('q', '')
    results = []
    if query:
        results = search_anime(query)
    return render_template('search.html', query=query, results=results)

@bp.route('/search/api')
def search_api():
    query = request.args.get('q', '')
    results = search_anime(query)
    
    # Если запрос на русском, попробуем транслитерацию
    if any(ord(c) > 127 for c in query):
        translit_query = translit(query)
        results_translit = search_anime(translit_query)
        # Объединяем результаты без дубликатов
        ids = {r['id'] for r in results}
        for r in results_translit:
            if r['id'] not in ids:
                results.append(r)
                ids.add(r['id'])
    
    return jsonify(results)

@bp.route('/settings')
def settings():
    return render_template('settings.html')

@bp.route('/mylist')
def mylist():
    return render_template('mylist.html')

@bp.route('/watch_history')
def watch_history():
    return render_template('watch_history.html')

@bp.route('/anime/<int:anime_id>')
def anime_detail(anime_id):
    anime = get_anime_by_id(anime_id)
    return render_template('anime.html', anime=anime)

@bp.route('/set_adult/<value>')
def set_adult(value):
    session['show_adult'] = value == 'true'
    return jsonify({'success': True})

@bp.route('/anime-page')
def anime_page():
    is_adult = session.get('show_adult', False)
    popular = get_popular_anime(is_adult=is_adult)
    trending = get_trending_anime(is_adult=is_adult)
    return render_template('anime_page.html', popular=popular, trending=trending)

@bp.route('/manga-page')
def manga_page():
    is_adult = session.get('show_adult', False)
    popular = get_popular_manga(is_adult=is_adult)
    trending = get_trending_manga(is_adult=is_adult)
    return render_template('manga_page.html', popular=popular, trending=trending)

@bp.route('/see_all/<content_type>')
def see_all(content_type):
    is_adult = session.get('show_adult', False)
    page = request.args.get('page', 1, type=int)
    
    if content_type == 'trending_anime':
        results = get_trending_anime(page=page, is_adult=is_adult)
        title = _('Trending Anime')
    elif content_type == 'popular_anime':
        results = get_popular_anime(page=page, is_adult=is_adult)
        title = _('Popular Anime')
    elif content_type == 'trending_manga':
        results = get_trending_manga(page=page, is_adult=is_adult)
        title = _('Trending Manga')
    elif content_type == 'popular_manga':
        results = get_popular_manga(page=page, is_adult=is_adult)
        title = _('Popular Manga')
    else:
        results = []
        title = ''
    
    return render_template('see_all.html', results=results, title=title, content_type=content_type, page=page)