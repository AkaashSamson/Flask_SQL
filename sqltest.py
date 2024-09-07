# from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# from sqlalchemy import Integer, String, Float

# class Base(DeclarativeBase):
#     pass

# db = SQLAlchemy(model_class=Base)

# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books-collection.db"

# db.init_app(app)

# class Book(db.Model):
#     id : Mapped[int] = mapped_column(Integer, primary_key=True)
#     title : Mapped[str] = mapped_column(String, nullable=False)
#     author : Mapped[str] = mapped_column(String, nullable=False)
#     rating : Mapped[float] = mapped_column(Float, nullable=False)

# with app.app_context():
#     db.create_all()

# with app.app_context():
#     new_book = Book(id=1, title="Harry Potter", author="J. K. Rowling", rating=9.3)
#     db.session.add(new_book)
#     db.session.commit()