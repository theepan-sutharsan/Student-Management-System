from flask import jsonify, request
from app.extensions import db
from app.models.enrollment_model import Enrollment


def _validate_enrollment_payload(data, enrollment_id=None):
    errors = []
    if not data:
        return ["Request body is required."]

    student_id = data.get("student_id")
    course_id = data.get("course_id")
    if student_id is None:
        errors.append("student_id is required.")
    if course_id is None:
        errors.append("course_id is required.")
    return errors

def create_enrollment():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    errors = _validate_enrollment_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        enrollment = Enrollment(
            student_id=data.get("student_id"),
            course_id=data.get("course_id"),
            status=data.get("status", "enrolled")
        )
        db.session.add(enrollment)
        db.session.commit()
        return jsonify({"message": "Enrollment created successfully.", "enrollment": enrollment.to_dict()}), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500

def get_enrollments():
    enrollments = Enrollment.query.all()
    return jsonify({"enrollments": [e.to_dict() for e in enrollments]}), 200

def get_enrollment(enrollment_id):
    enrollment = Enrollment.query.get(enrollment_id)
    if not enrollment:
        return jsonify({"error": "Enrollment not found."}), 404
    return jsonify({"enrollment": enrollment.to_dict()}), 200


def update_enrollment(enrollment_id):
    enrollment = Enrollment.query.get(enrollment_id)
    if not enrollment:
        return jsonify({"error": "Enrollment not found."}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided to update."}), 400

    errors = _validate_enrollment_payload(data, enrollment_id=enrollment_id)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        enrollment.student_id = data.get("student_id")
        enrollment.course_id = data.get("course_id")
        enrollment.status = data.get("status", "enrolled") 
        db.session.commit()
        return jsonify({"message": "Enrollment updated successfully.", "enrollment": enrollment.to_dict()}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500



def delete_enrollment(enrollment_id):
    enrollment = Enrollment.query.get(enrollment_id)
    if not enrollment:
        return jsonify({"error": "Enrollment not found."}), 404
    try:
        db.session.delete(enrollment)
        db.session.commit()
        return jsonify({"message": "Enrollment deleted successfully."}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500
