from flask import jsonify


def error_response(message, status=500):
    """Return a consistently shaped JSON error response."""
    return jsonify({"error": message}), status
