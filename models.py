import os
from flask import Flask, session, redirect, url_for, request, render_template, flash
from faker import Faker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import inspect

Base = declarative_base()  # Initialize the base class for SQLAlchemy models
fake = Faker('fr_CA')  # Set up Faker to generate Canadian French names
engine = create_engine('sqlite:///userCTF.db') # Create a new SQLite database or connect to an existing one
Session = sessionmaker(bind=engine) # Create a session factory bound to the database
session = Session() # Create an instance of the session class for database operations


class User(Base):  # Define a User model that will represent a table in the database
    __tablename__ = 'user'  # Set the name of the table in the database
    id = Column(Integer, primary_key=True)  # Create a primary key column for the table
    username = Column(String(80), unique=True, nullable=False)  # Create a column for the username, which must be unique and not null
    password = Column(String(120), nullable=False)  # Create a column for the password, which is not null
    full_name = Column(String(120), nullable=False)  # Create a column for the user's full name, which is not null


def create_db_and_populate():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    inspector = inspect(engine)
    if not inspector.has_table('user'):
        Base.metadata.tables['user'].create(bind=engine)

    secret_user = User(username="User", password="Qwerty!", full_name= fake.name())  # Create a secret user with a default username and password
    session.add(secret_user)  # Add the secret user to the session for insertion into the database

    # Add 50 employees to the database with randomly generated names, usernames, and passwords
    for _ in range(50):
        name = fake.name()
        first_name, last_name = name.split()
        username = f"{first_name[0].upper()}{last_name.lower()}"
        password = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
        employee = User(full_name=name, username=username, password=password)
        session.add(employee)

    # Add an administrator to the database with a randomly generated name, username, and password
    admin_full_name = fake.name()
    admin = User(full_name=admin_full_name, username='MasterAdminFullPower', password=fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True))
    session.add(admin)

    session.commit()  # Commit all changes to the database

users = session.query(User).all()
for user in users:
    print(f"ID:{user.id} Username: {user.username} Password :{user.password} Name : {user.full_name}")

