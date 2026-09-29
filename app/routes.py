from flask import Blueprint, render_template, request, session, jsonify
from app.anilist_api import search_anime, get_anime_by_id, get_popular_anime, get_trending_anime

bp = Blueprint('main', __name__)

@bp.route('/set_language/<lang>')
def set_language(lang):
    if lang in ['en', 'ru']:
        session['language'] = lang
    return jsonify({'success': True})

@bp.route('/')
def index():
    popular = get_popular_anime()
    trending = get_trending_anime()
    featured = trending[:10] if trending else []
    return render_template('index.html', popular=popular, trending=trending, featured=featured)

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

@bp.route('/anime/<int:anime_id>')
def anime_detail(anime_id):
    anime = get_anime_by_id(anime_id)
    return render_template('anime.html', anime=anime)