from app import create_app
from flask_cors import CORS

app = create_app()
CORS(app)

@app.route('/')
def home ():
    return '<h1>This is Home Page</h1>'

if __name__ == "__main__":
    with app.app_context():
        from app.extensions import db
        db.create_all()
    
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

