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
app.run(port=8080)
