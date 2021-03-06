from flask import render_template,jsonify

from app import app

@app.errorhandler(404)
def not_found_error(error):
    app.logger.warn(error)
    return jsonify({'response':'404: not found'}),404


@app.errorhandler(500)
def internal_error(error):
    #cleanup?
    app.logger.error(error)
    return jsonify({'response':f'500 error {error}'}), 500