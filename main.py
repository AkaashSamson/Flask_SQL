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

class base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=base)

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
Bootstrap5(app)

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



# CREA DB


# CREATE TABLE


@app.route("/")
def home():
    with app.app_context():
        movies = db.session.execute(db.select(Movie))
        all_movies = movies.scalars()
        return render_template("index.html", movies=all_movies)


if __name__ == '__main__':
    app.run(debug=True)
