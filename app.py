import click

from flask import Flask,render_template
from flask_bootstrap import Bootstrap

from datetime import timedelta

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
# app.config['DEBUG'] = True

if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

bootstrap = Bootstrap(app)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.cli.command()
def delete_cache():
    pass


if __name__ == '__main__':
    app.run()
