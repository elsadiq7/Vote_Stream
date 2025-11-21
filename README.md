# FastAPI Posts API

A robust and high-performance RESTful API built with [FastAPI](https://fastapi.tiangolo.com/) for managing posts, users, and votes. This project includes authentication, database migrations, and containerization support.

## 🚀 Features

*   **User Management**: User registration and profile management.
*   **Authentication**: Secure JWT (JSON Web Token) authentication.
*   **Posts**: Create, read, update, and delete posts.
*   **Voting System**: Like/dislike or upvote/downvote functionality for posts.
*   **Database**: PostgreSQL integration using SQLAlchemy ORM.
*   **Migrations**: Database schema migrations with Alembic.
*   **Validation**: Data validation using Pydantic.
*   **Dockerized**: Ready-to-use Docker Compose setup for development and production.

## 🛠️ Tech Stack

*   **Framework**: FastAPI
*   **Language**: Python 3.9+
*   **Database**: PostgreSQL
*   **ORM**: SQLAlchemy
*   **Migrations**: Alembic
*   **Authentication**: OAuth2 with Password (and Hashing with Bcrypt)
*   **Containerization**: Docker & Docker Compose

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

*   [Docker](https://www.docker.com/get-started) & [Docker Compose](https://docs.docker.com/compose/install/) (Recommended)
*   [Python 3.9+](https://www.python.org/downloads/) (If running locally)
*   [PostgreSQL](https://www.postgresql.org/download/) (If running locally)

## 🔧 Configuration

The application requires the following environment variables. You can set them in a `.env` file in the root directory.

| Variable | Description | Example |
| :--- | :--- | :--- |
| `DATABASE_HOSTNAME` | Database host address | `localhost` or `postgres` (in Docker) |
| `DATABASE_PORT` | Database port | `5432` |
| `DATABASE_PASSWORD` | Database password | `password123` |
| `DATABASE_NAME` | Database name | `fastapi` |
| `DATABASE_USERNAME` | Database username | `postgres` |
| `SECRET_KEY` | Secret key for JWT signing | `your_secret_key_here` |
| `ALGORITHM` | Encryption algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |

## 🚀 Getting Started

### Option 1: Using Docker (Recommended)

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Run with Docker Compose:**
    This command will start the API and a PostgreSQL database container.
    ```bash
    docker-compose -f docker-compose-dev.yaml up -d --build
    ```

3.  **Access the API:**
    The API will be available at `http://localhost:8000`.

### Option 2: Local Development

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the root directory and add the variables listed in the **Configuration** section. Ensure you have a running PostgreSQL instance.

5.  **Run Database Migrations:**
    ```bash
    alembic upgrade head
    ```

6.  **Start the Server:**
    ```bash
    uvicorn app.main:app --reload
    ```

## 📚 API Documentation

FastAPI automatically generates interactive API documentation. Once the server is running, you can access:

*   **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs) - Interactive exploration and testing of API endpoints.
*   **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc) - Alternative documentation view.

## 📂 Project Structure

```
.
├── app/
│   ├── routers/        # API route handlers (auth, post, user, vote)
│   ├── config.py       # Environment configuration
│   ├── database.py     # Database connection setup
│   ├── main.py         # Application entry point
│   ├── models.py       # SQLAlchemy database models
│   ├── outh2.py        # Authentication logic
│   ├── schemas.py      # Pydantic schemas for request/response
│   └── utils.py        # Utility functions (hashing, etc.)
├── alembic/            # Database migration scripts
├── docker-compose-dev.yaml  # Docker Compose for development
├── Dockerfile          # Docker image definition
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## 🗄️ Database Migrations

This project uses **Alembic** for database migrations.

*   **Create a new migration:**
    ```bash
    alembic revision --autogenerate -m "message"
    ```
*   **Apply migrations:**
    ```bash
    alembic upgrade head
    ```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the project
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request
