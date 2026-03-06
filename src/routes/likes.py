from flask import Blueprint, jsonify, request, g
from src.config.db import get_db
from src.middleware.auth import verify_token

likes_bp = Blueprint('likes', __name__)

@likes_bp.route('/toggle', methods=['POST'])
@verify_token
def toggle_like():
    try:
        user_id = g.user.get('id')
        data = request.get_json(silent=True) or {}
        design_id = data.get('design_id')

        with get_db() as db:
            existing = db.execute(
                'SELECT * FROM likes WHERE user_id = ? AND design_id = ?', 
                (user_id, design_id)
            ).fetchone()

            if existing:
                db.execute('DELETE FROM likes WHERE user_id = ? AND design_id = ?', (user_id, design_id))
                return jsonify({'message': 'Unliked', 'liked': False})
            else:
                db.execute('INSERT INTO likes (user_id, design_id) VALUES (?, ?)', (user_id, design_id))
                return jsonify({'message': 'Liked', 'liked': True})

    except Exception as e:
        print('Error in toggleLike:', e)
        return jsonify({'error': 'Action failed'}), 500

@likes_bp.route('/me', methods=['GET'])
@verify_token
def get_liked_designs():
    try:
        user_id = g.user.get('id')
        with get_db() as db:
            liked_designs = db.execute('''
                SELECT d.* FROM likes l
                JOIN designs d ON l.design_id = d.design_id
                WHERE l.user_id = ?
            ''', (user_id,)).fetchall()
            return jsonify([dict(d) for d in liked_designs])
    except Exception as e:
        print('Error in getLikedDesigns:', e)
        return jsonify({'error': 'Failed to fetch likes'}), 500

@likes_bp.route('/status/<int:design_id>', methods=['GET'])
@verify_token
def get_like_status(design_id):
    try:
        user_id = g.user.get('id')
        with get_db() as db:
            exists = db.execute(
                'SELECT 1 FROM likes WHERE user_id = ? AND design_id = ?', 
                (user_id, design_id)
            ).fetchone()
            return jsonify({'liked': bool(exists)})
    except Exception as e:
        print('Error in getLikeStatus:', e)
        return jsonify({'error': 'Failed to fetch like status'}), 500
