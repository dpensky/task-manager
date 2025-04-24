# 📝 Task Manager Web App

A simple full-stack task management application that allows users to register, log in, and manage their to-do tasks. Built with **FastAPI** for the backend and **JavaScript** for the frontend.

Test it here: https://task-manager-99m1.onrender.com/

---

## 🔧 Features

- ✅ User registration and login
- 📝 Add new tasks (title + description)
- 📋 View all tasks
- ✅ Mark tasks as completed
- ❌ Delete tasks
- 🔐 Authentication with JWT tokens

---

## 💻 Tech Stack

**Frontend:**
- HTML, CSS, JavaScript (Vanilla or React)

**Backend:**
- Python
- [FastAPI](https://fastapi.tiangolo.com/)
- SQLite (via SQLAlchemy)

**Other Tools:**
- Git & GitHub
- Render/Vercel (for hosting)
- Postman (for API testing)

**Requirements:**
- fastapi – The core web framework
- uvicorn – ASGI server to run FastAPI
- sqlalchemy – ORM for working with SQLite (or other DBs)
- pydantic – Data validation and serialization (used by FastAPI)
- passlib[bcrypt] – For securely hashing passwords
- python-jose – To create and verify JWT tokens for authentication

---
## 📂 Project Structure
```
task-manager
├── backend
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── LICENSE
├── README.md
├── requirements.txt
└── static
    ├── app.js
    ├── index.html
    └── style.css
```
