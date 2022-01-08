from flask import render_template


def error_404(e):
    return render_template('errors/error_404.html', title="404 Not Found"), 404
