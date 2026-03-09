from flask import Blueprint, jsonify, request
from src.config.db import get_db

discovery_bp = Blueprint('discovery', __name__)

@discovery_bp.route('/', methods=['GET'], strict_slashes=False)
@discovery_bp.route('', methods=['GET'])
def get_curated_designs():
    try:
        category = request.args.get('category')
        # occasion = request.args.get('occasion')  # Column doesn't exist yet
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')
        min_weight = request.args.get('min_weight')
        max_weight = request.args.get('max_weight')

        with get_db() as db:
            rates = db.execute('SELECT * FROM gold_rates ORDER BY updated_at DESC').fetchall()
            rate_map = {'22K': 6200, '24K': 6800}
            for r in rates:
                if r['purity'] not in rate_map or r == rates[0]: # Rough equivalent of JS reduce
                     rate_map[r['purity']] = float(r['rate_per_gram'])

            first_images = db.execute('''
                SELECT design_id, MIN(media_id) as first_media_id 
                FROM design_media 
                WHERE is_primary = 1 OR type = 'image'
                GROUP BY design_id
            ''').fetchall()

            image_map = {}
            for img in first_images:
                media = db.execute('SELECT url FROM design_media WHERE media_id = ?', (img['first_media_id'],)).fetchone()
                if media:
                    image_map[img['design_id']] = media['url']

            like_counts = db.execute('SELECT design_id, COUNT(*) as likes_count FROM likes GROUP BY design_id').fetchall()
            like_map = {l['design_id']: l['likes_count'] for l in like_counts}

            query = '''
                SELECT d.*, s.business_name, s.city, s.trust_score
                FROM designs d
                JOIN sellers s ON d.seller_id = s.seller_id
                WHERE d.availability_status = 'available' AND d.media_quality_status = 'approved'
            '''
            params = []

            if category:
                query += ' AND d.category = ?'
                params.append(category)
            # if occasion:
            #     query += ' AND d.occasion_tag = ?'
            #     params.append(occasion)
            if min_weight:
                query += ' AND d.weight >= ?'
                params.append(float(min_weight))
            if max_weight:
                query += ' AND d.weight <= ?'
                params.append(float(max_weight))

            designs = db.execute(query, tuple(params)).fetchall()

            enriched_designs = []
            for design in designs:
                current_rate = rate_map.get(design['purity'], rate_map.get('22K', 6200))
                gold_value = design['weight'] * current_rate
                subtotal = gold_value + design['making_charge_snapshot']
                gst = subtotal * 0.03
                total_price = subtotal + gst

                # Create dictionary representation matching JS map output
                d_dict = dict(design)
                d_dict.update({
                    'name': f"{design['purity']} Gold {design['category']}",
                    'seller_name': design['business_name'],
                    'views_count': design['view_count'],
                    'occasion': None,  # Column doesn't exist yet
                    'making_charge': design['making_charge_snapshot'],
                    'gold_rate': current_rate,
                    'current_gold_rate': current_rate,
                    'gold_value': gold_value,
                    'total_price': total_price,
                    'total_price_display': total_price,
                    'gst': gst,
                    'likes_count': like_map.get(design['design_id'], 0),
                    'primary_image_url': image_map.get(design['design_id']),
                    'master_image': image_map.get(design['design_id'])
                })
                enriched_designs.append(d_dict)

            filtered = enriched_designs
            # Remove designs without images
            filtered = [d for d in filtered if d['primary_image_url']]
            
            if min_price:
                filtered = [d for d in filtered if d['total_price'] >= float(min_price)]
            if max_price:
                filtered = [d for d in filtered if d['total_price'] <= float(max_price)]

            return jsonify(filtered)

    except Exception as e:
        print('[DISCOVERY] Error fetching designs:', e)
        return jsonify({'error': 'Failed to fetch curated designs'}), 500

@discovery_bp.route('/<int:id>', methods=['GET'])
def get_design_by_id(id):
    try:
        with get_db() as db:
            rates = db.execute('SELECT * FROM gold_rates ORDER BY updated_at DESC').fetchall()
            rate_map = {'22K': 6200, '24K': 6800}
            for r in rates:
                rate_map[r['purity']] = float(r['rate_per_gram'])

            design = db.execute('''
                SELECT d.*, s.business_name, s.city, s.trust_score, s.seller_id as sid
                FROM designs d
                JOIN sellers s ON d.seller_id = s.seller_id
                WHERE d.design_id = ?
            ''', (id,)).fetchone()

            if not design:
                return jsonify({'error': 'Design not found'}), 404

            media = db.execute('''
                SELECT * FROM design_media 
                WHERE design_id = ?
                ORDER BY is_primary DESC, media_id ASC
            ''', (id,)).fetchall()

            db.execute('UPDATE designs SET view_count = view_count + 1 WHERE design_id = ?', (id,))

            current_rate = rate_map.get(design['purity'], rate_map.get('22K', 6200))
            gold_value = design['weight'] * current_rate
            making_charge = design['making_charge_snapshot']
            subtotal = gold_value + making_charge
            gst = subtotal * 0.03
            total_price = subtotal + gst

            result = dict(design)
            result.update({
                'current_gold_rate': current_rate,
                'media': [{'shot_type': m['type'], 'uri': m['url'], **{k: v for k, v in dict(m).items() if k not in ['type', 'url']}} for m in media],
                'total_price': total_price,
                'total_price_display': total_price,
                'price_breakdown': {
                    'reference_rate': current_rate,
                    'weight': design['weight'],
                    'gold_value': gold_value,
                    'making_charge': making_charge,
                    'gst': gst,
                    'total': total_price
                }
            })
            
            return jsonify(result)

    except Exception as e:
        print('[DISCOVERY] Error fetching design detail:', e)
        return jsonify({'error': 'Failed to fetch design detail'}), 500
