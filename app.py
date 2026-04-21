import os
from flask import Flask, send_from_directory, request, redirect
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask App
app = Flask(__name__, static_folder='public', static_url_path='')

PORT = int(os.environ.get('PORT', 5001))

# 1. Security Headers Middleware
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

# 2. HTTPS Enforcement (Redirect in Production)
@app.before_request
def enforce_https():
    if os.environ.get('NODE_ENV') == 'production' and request.headers.get('x-forwarded-proto') != 'https':
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)

# 3. Request Logging Middleware
@app.before_request
def log_request_info():
    # Similar to Node.js simple logger
    print(f"[REQUEST] {request.method} {request.path}")

# Middleware Configuration
CORS(app)

# 4. API ROUTES GO HERE (will be registered as blueprints)
from src.routes.auth import auth_bp
from src.routes.wallet import wallet_bp
from src.routes.likes import likes_bp
from src.routes.discovery import discovery_bp
from src.routes.intent import intent_bp
from src.routes.appointment import appointment_bp
from src.routes.admin import admin_bp
from src.routes.health import health_bp
from src.routes.seller import seller_bp
from src.routes.payment import payment_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(wallet_bp, url_prefix='/api/wallet')
app.register_blueprint(likes_bp, url_prefix='/api/likes')
app.register_blueprint(discovery_bp, url_prefix='/api/designs')
app.register_blueprint(intent_bp, url_prefix='/api/blocks')
app.register_blueprint(appointment_bp, url_prefix='/api/appointments')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(health_bp, url_prefix='/api/health')
app.register_blueprint(seller_bp, url_prefix='/api/sellers')
app.register_blueprint(payment_bp, url_prefix='/api/pay')

# 5. FRONTEND STATIC & PAGE ROUTES
@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    # uploads directory is expected to be alongside public/
    uploads_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    return send_from_directory(uploads_dir, filename)

# 6. HTML File Serving Routes (mimicking express app.get('/', serve('index.html')))
def serve_html(filename):
    return app.send_static_file(filename)

@app.route('/')
def index(): return serve_html('index.html')

@app.route('/collection')
def collection(): return serve_html('collection.html')

@app.route('/design/<id>')
def design_detail(id): return serve_html('detail.html')

@app.route('/seller/<id>')
def seller_detail(id): return serve_html('seller.html')

@app.route('/wallet')
def wallet(): return serve_html('wallet.html')

@app.route('/seller-dashboard')
def seller_dashboard(): return serve_html('seller-dashboard.html')

@app.route('/seller-register')
def seller_register(): return serve_html('seller-register.html')

@app.route('/admin')
def admin(): return serve_html('admin.html')

@app.route('/login')
@app.route('/seller-login')
@app.route('/admin-login')
def login(): return serve_html('login.html')

@app.route('/intent-path')
def intent_path(): return serve_html('scheduling.html')

@app.route('/how-it-works')
def how_it_works(): return serve_html('how-it-works.html')

@app.route('/problem')
def problem(): return serve_html('problem.html')

@app.route('/about')
def about(): return serve_html('about.html')

@app.route('/philosophy')
def philosophy(): return serve_html('philosophy.html')

@app.route('/profile/likes')
def profile_likes(): return serve_html('profile/likes.html')

# Legal Routes
@app.route('/terms')
def terms(): return serve_html('terms.html')

@app.route('/wallet-policy')
def wallet_policy(): return serve_html('wallet-policy.html')

@app.route('/seller-agreement')
def seller_agreement(): return serve_html('seller-agreement.html')


if __name__ == '__main__':
    print('--- SYSTEM BOOT SUCCESSFUL ---')
    print(f'[BOOT] MODE: STATEFUL APPLICATION')
    print(f'[BOOT] HOST: http://localhost:{PORT}')
    print('STATIC ENABLED')
    print('MULTIPAGE ROUTING ENABLED')

    # Initialize Background Workers (APScheduler)
    try:
        if not os.environ.get("WERKZEUG_RUN_MAIN"):
            from src.workers.workers import start_workers
            start_workers()
    except Exception as e:
        print("[WORKER] Failed to start background workers:", e)
    
    app.run(port=PORT, debug=True)
