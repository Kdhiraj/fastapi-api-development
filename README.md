# 🚀 FastAPI API Development

![Stars](https://img.shields.io/github/stars/Kdhiraj/fastapi-api-development?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-109989?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

This repository contains my **personal learning journey with FastAPI**, where I go beyond basic CRUD and explore real-world backend development concepts.

⭐ **Please give this repository a star if you find it useful or inspiring!**

---

## 🔹 Concepts Covered

This project explores and practices:

- FastAPI core & advanced features
- Pydantic models & validation
- JWT authentication
- Authentication & Authorization
- Role-Based Access Control (RBAC)
- SQLAlchemy ORM
- SQLModel
- Dependency Injection
- Environment configuration
- API security best practices
- Database Migration

---

## 🔹 Tech Stack

- **FastAPI** — modern Python framework for APIs :contentReference[oaicite:2]{index=2}
- **Python 3.10+**
- **uv** (fast Python package & environment manager)
- **PostgreSQL**
- **SQLAlchemy & SQLModel**
- **Pydantic**
- **JWT**
- **Alembic**

---

## 📑 Table of Contents

1. [Getting Started](#getting-started)
2. [Prerequisites](#prerequisites)
3. [Project Setup](#project-setup)
4. [Running the Application](#running-the-application)
5. [Running Tests](#running-tests)
6. [Contributing](#contributing)
7. [Support](#support)

---

## Getting Started

Follow the instructions below to set up and run the project locally.

---

## Prerequisites

Make sure you have:

- Python **>= 3.10**
- PostgreSQL
- Git
- `uv` installed

Install uv (if not already installed):

```bash
pip install uv
```

## Project Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Kdhiraj/fastapi-api-development.git
   ```
2. Navigate to the project directory:

   ```bash
   cd fastapi-api-development
   ```

3. Create a virtual environment using uv:

   ```bash
   uv venv
   source .venv/bin/activate   # Linux / macOS
   .venv\Scripts\activate     # Windows
   ```

4. Install dependencies:

   ```bash
   uv pip install -r requirements.txt
   or
   uv sync
   ```

5. Create environment variables:

   ```bash
   cp .env.example .env
   ```

6. Edit .env with your database URL, secret keys, and configuration.

7. Intialize database migrations
   ```bash
   alembic init -t async migrations
   ```
8. Run database migrations (if using Alembic):
   ```bash
   alembic upgrade head
   ```

## Running the Application

Start the development server:

```bash
fastapi dev src/
```

Or using Uvicorn directly:

```bash
uvicorn src.main:app --reload
```

Alternatively, you can run the application using Docker:

```bash
docker compose up -d
```

## Running Tests

Run the tests using this command:

```bash
pytest
```

## API Documentation

Open your browser at:

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

## Contributing

This is a personal learning project, but suggestions and improvements are welcome.

### Feel free to:

- Open issues
- Suggest improvements
- Submit pull requests

## Support

If you found this repository helpful:
Please give it a star — it really motivates me to keep learning and improving! ⭐
