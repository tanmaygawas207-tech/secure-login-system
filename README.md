# Secure Login System

## About

A basic secure login web application developed as part of the Thirenax Virtual Cyber Security Internship.

## Features

- User registration
- User login
- Password hashing using bcrypt
- Input validation
- SQL injection protection
- Session management
- Logout functionality

## Technologies Used

- Python
- Flask
- SQLite
- bcrypt
- HTML

## Security Features

### Password Hashing

Passwords are hashed using bcrypt before being stored in the database.

### SQL Injection Protection

Parameterized SQL queries are used instead of directly inserting user input into SQL statements.

### Session Management

Flask sessions are used to maintain authenticated users.

### Input Validation

The application checks username and password requirements during registration.

## How to Run

Install the required packages:

```text
pip install -r requirements.txt

Run the application:
python app.py
