from app.routes.student_routes import student_bp
from app.routes.lecturer_routes import lecturer_bp
def register_blueprints(app):
    app.register_blueprint(student_bp)
    app.register_blueprint(lecturer_bp)