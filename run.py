from app import create_app

app = create_app()

@app.route('/')
def home ():
    return '<h1>This is Home Page</h1>'

if __name__ == "__main__":
    try:
        with app.app_context():
            from app.extensions import db
            db.create_all() 
            print("SUCCESS: Database Connected Successfully")
           

    except Exception as e:
        print("ERROR: Database Connection Failed")
        print(e)
    app.run(debug=True,port=8080)
