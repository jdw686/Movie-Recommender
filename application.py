from flask import Flask
from flask import render_template
from flask import request
from recommendations import get_recommendations

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html', movies_html=[])


@app.route('/get_recommendations')
def recommender():
    """docstring"""
    user_movies = [request.args['movie1'], request.args['movie2'], request.args['movie3']]
    user_rating = [request.args['rating1'], request.args['rating2'], request.args['rating3']]

    movies = get_recommendations(user_movies, user_rating)
    title = "The next movie you want to watch is: "
    return render_template('recommendations.html', movies_html=movies, title=title)
