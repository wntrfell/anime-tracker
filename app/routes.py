from flask import Blueprint, render_template, request, session, jsonify
from app.anilist_api import (
    search_anime, get_anime_by_id, 
    get_popular_anime, get_trending_anime,
    get_popular_manga, get_trending_manga
)

bp = Blueprint('main', __name__)

@bp.route('/set_language/<lang>')
def set_language(lang):
    if lang in ['en', 'ru']:
        session['language'] = lang
    return jsonify({'success': True})

@bp.route('/set_adult/<value>')
def set_adult(value):
    session['show_adult'] = value == 'true'
    return jsonify({'success': True})

@bp.route('/')
def index():
    is_adult = session.get('show_adult', False)
    
    # Главная страница - всегда 24 постера (2 ряда по 12)
    popular = get_popular_anime(per_page=24, is_adult=is_adult)
    trending = get_trending_anime(per_page=24, is_adult=is_adult)
    popular_manga = get_popular_manga(per_page=24, is_adult=is_adult)
    trending_manga = get_trending_manga(per_page=24, is_adult=is_adult)
    
    featured = trending[:10] if trending else []
    
    return render_template('index.html', 
                          popular=popular, 
                          trending=trending,
                          popular_manga=popular_manga, 
                          trending_manga=trending_manga,
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

@bp.route('/anime-page')
def anime_page():
    is_adult = session.get('show_adult', False)
    page = request.args.get('page', 1, type=int)
    # Страница аниме - 72 постера (6 рядов по 12)
    popular = get_popular_anime(page=page, per_page=48, is_adult=is_adult)
    return render_template('anime_page.html', items=popular, page=page, content_type='anime')

@bp.route('/manga-page')
def manga_page():
    is_adult = session.get('show_adult', False)
    page = request.args.get('page', 1, type=int)
    # Страница манги - 72 постера (6 рядов по 12)
    popular = get_popular_manga(page=page, per_page=48, is_adult=is_adult)
    return render_template('manga_page.html', items=popular, page=page, content_type='manga')

@bp.route('/see_all/<content_type>')
def see_all(content_type):
    is_adult = session.get('show_adult', False)
    page = request.args.get('page', 1, type=int)
    
    if content_type == 'trending_anime':
        results = get_trending_anime(page=page, is_adult=is_adult)
        title = 'Trending Anime'
    elif content_type == 'popular_anime':
        results = get_popular_anime(page=page, is_adult=is_adult)
        title = 'Popular Anime'
    elif content_type == 'trending_manga':
        results = get_trending_manga(page=page, is_adult=is_adult)
        title = 'Trending Manga'
    elif content_type == 'popular_manga':
        results = get_popular_manga(page=page, is_adult=is_adult)
        title = 'Popular Manga'
    else:
        results = []
        title = ''
    
    return render_template('see_all.html', results=results, title=title, content_type=content_type, page=page)

@bp.route('/anime/<int:anime_id>')
def anime_detail(anime_id):
    anime = get_anime_by_id(anime_id)
    return render_template('anime.html', anime=anime)