from flask import Blueprint, render_template, request, session, jsonify
from app.anilist_api import search_anime, get_anime_by_id

bp = Blueprint('main', __name__)

@bp.route('/set_language/<lang>')
def set_language(lang):
    if lang in ['en', 'ru']:
        session['language'] = lang
    return jsonify({'success': True})

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/search')
def search():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    results = search_anime(query, page)
    return jsonify(results)

@bp.route('/anime/<int:anime_id>')
def anime_detail(anime_id):
    anime = get_anime_by_id(anime_id)
    return render_template('anime.html', anime=anime)