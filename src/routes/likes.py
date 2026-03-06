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
            rates = db.execute('SELECT * FROM gold_rates ORDER BY updated_at DESC').fetchall()
            rate_map = {'22K': 6200, '24K': 6800}
            for r in rates:
                if r['purity'] not in rate_map or r == rates[0]:
                     rate_map[r['purity']] = float(r['rate_per_gram'])

            first_images = db.execute('''
                SELECT design_id, MIN(media_id) as first_media_id 
                FROM design_media 
                WHERE shot_type = 'master' AND status = 'approved' 
                GROUP BY design_id
            ''').fetchall()

            image_map = {}
            for img in first_images:
                media = db.execute('SELECT uri FROM design_media WHERE media_id = ?', (img['first_media_id'],)).fetchone()
                if media:
                    image_map[img['design_id']] = media['uri']

            liked_designs = db.execute('''
                SELECT d.*, s.business_name, s.city, s.trust_score
                FROM likes l
                JOIN designs d ON l.design_id = d.design_id
                JOIN sellers s ON d.seller_id = s.seller_id
                WHERE l.user_id = ?
            ''', (user_id,)).fetchall()

            enriched_designs = []
            for design in liked_designs:
                current_rate = rate_map.get(design['purity'], rate_map.get('22K', 6200))
                gold_value = design['weight'] * current_rate
                subtotal = gold_value + design['making_charge_snapshot']
                gst = subtotal * 0.03
                total_price = subtotal + gst

                d_dict = dict(design)
                d_dict.update({
                    'name': f"{design['purity']} Gold {design['category']}",
                    'seller_name': design['business_name'],
                    'views_count': design['view_count'],
                    'occasion': design['occasion_tag'],
                    'making_charge': design['making_charge_snapshot'],
                    'gold_rate': current_rate,
                    'current_gold_rate': current_rate,
                    'gold_value': gold_value,
                    'total_price': total_price,
                    'total_price_display': total_price,
                    'gst': gst,
                    'primary_image_url': image_map.get(design['design_id']),
                    'master_image': image_map.get(design['design_id'])
                })
                enriched_designs.append(d_dict)

            # Remove designs without images
            filtered = [d for d in enriched_designs if d['primary_image_url']]

            return jsonify(filtered)
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
