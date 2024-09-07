from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books-collection.db"

db.init_app(app)

class Book(db.Model):
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    title : Mapped[str] = mapped_column(String, nullable=False, unique=True)
    author : Mapped[str] = mapped_column(String, nullable=False)
    rating : Mapped[float] = mapped_column(Float, nullable=False)

#all_books = []
with app.app_context():
    db.create_all()

# with app.app_context():
#     #delete all records
#     books = db.session.execute(db.select(Book))
#     for book in books.scalars():
#         db.session.delete(book)
#     db.session.commit()


@app.route('/', methods=["GET", "POST"])
def home():        
    with app.app_context():
        all_books = []
        books = []
        books = db.session.execute(db.select(Book))
        all_books = books.scalars()
        return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        with app.app_context():
            book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
            )
            db.session.add(book)
            db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")

#to pass varaiables in the url, use <variable_name> and further we can use variable name in the function
#for example here we are passing bookid in the url


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        with app.app_context():
            book_id = request.args.get("id")
            new_rating = request.form["newrating"]
            db.session.execute(db.update(Book).where(Book.id == book_id).values(rating=new_rating))
            db.session.commit()
        return redirect(url_for('home'))
    
    with app.app_context():
        #index page passes book id as a paraeter for url_for in order to retrieve it here
        book_id = request.args.get("id")
        print(book_id)
        #To retrieve the title of the book
        result = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
        title = result.title
        return render_template("edit.html", bktitle=title, bkid = book_id)

@app.route("/delete", methods=["GET", "POST"])
def delete():
    with app.app_context():
        book_id = request.args.get("id")
        book = db.session.execute(db.select(Book).where(Book.id == book_id))
        db.session.delete(book.scalar())
        db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

