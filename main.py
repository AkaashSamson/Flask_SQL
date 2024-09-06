from flask import Flask, render_template, request, redirect, url_for



app = Flask(__name__)

all_books = []


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        book = {
            "title": request.form["title"],
            "author": request.form["author"],
            "rating": request.form["rating"]
        }
        all_books.append(book)
        return render_template("index.html", books=all_books)
    return render_template("index.html", books=all_books)


@app.route("/add")
def add():
    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)

