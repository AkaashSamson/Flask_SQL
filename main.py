from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

url = "https://api.themoviedb.org/3/search/movie?query="

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlYjExNTkwNGQxNzFmNTUyYTM1ZDcyY2VmYWNlMjk0OCIsIm5iZiI6MTcyNTk3ODI4NS4xNzE3NDYsInN1YiI6IjY2ZGZkOWFlMDAwMDAwMDAwMGE0Njk2OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.o4PCjZY6YFtTYDkB47iLBPbsQPbRP9iHYaXz8e0OQhw"
}

class base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=base)

app = Flask(__name__)
app.secret_key = "randomrubbishstring"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'

bootstrap = Bootstrap5(app)
db.init_app(app)

class Movie(db.Model):
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    title : Mapped[str] = mapped_column(String, unique=True, nullable=False)
    year : Mapped[int] = mapped_column(Integer, nullable=False)
    description : Mapped[str] = mapped_column(String, nullable=False)
    rating : Mapped[float] = mapped_column(Float, nullable=False)
    ranking : Mapped[int] = mapped_column(Integer, nullable=False)
    review : Mapped[str] = mapped_column(String, nullable=False)
    img_url : Mapped[str] = mapped_column(String, nullable=False)

with app.app_context():
    db.create_all()

#ADDING A MOVIE
# new_movie = Movie(
#     title="Up",
#     year=2009,
#     description="Seventy-eight-year-old Carl Fredricksen travels to Paradise Falls in his house equipped with balloons, inadvertently taking a young stowaway.",
#     rating=8.2,
#     ranking=9,
#     review="One of the most emotional movies to ever exist.",
#     img_url="https://upload.wikimedia.org/wikipedia/en/0/05/Up_%282009_film%29.jpg"
# )
  
# with app.app_context():
#     db.session.add(new_movie)
#     db.session.commit()


class EditForm(FlaskForm):
    review = StringField("Review")
    rating = StringField("Rating")
    image_url = StringField("Image URL")
    submit = SubmitField("Done")

class AddForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")


@app.route("/")
def home():
    with app.app_context():
        movies = db.session.execute(db.select(Movie))
        all_movies = movies.scalars()
        return render_template("index.html", movies=all_movies)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    edit_form = EditForm()
    movie_title = request.args.get("title")
    movie_id = request.args.get("id")
    if edit_form.validate_on_submit():
        with app.app_context():
            movie = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
            if edit_form.image_url.data:
                movie.img_url = edit_form.image_url.data
            if edit_form.rating.data:
                movie.rating = edit_form.rating.data
            if edit_form.review.data:
                movie.review = edit_form.review.data
            db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=edit_form, m_title=movie_title, m_id=movie_id)

@app.route("/delete")
def delete():
    movie_id = request.args.get("id")
    with app.app_context():
        movie = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
        db.session.delete(movie)
        db.session.commit()
    return redirect(url_for('home'))


@app.route("/add", methods=["GET", "POST"])
def add():
    add_form = AddForm()
    if add_form.validate_on_submit():
        title = add_form.title.data
        response = requests.get(url + "'"+title+"'", headers=headers)
        data = response.json()
        #to get the list of objects reults from json data

        movie_data = data["results"] 
        return render_template("select.html", data=movie_data)
    return render_template("add.html", form=add_form)

@app.route("/select", methods=["GET", "POST"])
def select():
    movie_data = request.args.get("Movie")
    with app.app_context():
        # year = movie_data.release_date
        new_movie = Movie(
    title=movie_data.title,
    year=movie_data.release_date,
    description=movie_data.overview,
    rating=movie_data.vote_average,
    ranking=movie_data.popularity,
    review="",
    img_url=movie_data.poster_path
   )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
