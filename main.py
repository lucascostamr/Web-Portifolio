from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/projects")
def projects():
    return render_template("projects.html")


if __name__ == '__main__':
    app.run(debug=True)
