# Minimalist Daily Task List Application

A simple, production-ready daily task list application built with FastAPI, SQLite, and Jinja2. It features a minimalist, mobile-first design that scales to a "paper-like" desktop view.

## Project Structure
```
.
├── main.py              # ALL application code (FastAPI, SQLAlchemy models, routes)
├── requirements.txt     # Dependencies
├── Dockerfile           # Deployment configuration
├── README.md            # Documentation
└── templates/
    ├── base.html        # Layout with embedded CSS
    └── index.html       # Main task list view
```

## How to Run Locally

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    python main.py
    ```

    The application will be accessible at `http://localhost:8000`.

## How to Run with Docker

1.  **Build the Docker image:**
    ```bash
    docker build -t daily-tasks .
    ```

2.  **Run the Docker container:**
    ```bash
    docker run -p 8000:8000 daily-tasks
    ```

    The application will be accessible at `http://localhost:8000`.

## Endpoints

*   `GET /`: Render the main task list view.
*   `POST /add`: Add a new task. Expects form data with a `content` field.
*   `POST /toggle/{task_id}`: Toggle the completion status of a task. Replace `{task_id}` with the actual task ID.
*   `POST /delete/{task_id}`: Delete a task. Replace `{task_id}` with the actual task ID.
*   `GET /health`: Returns `{"status": "ok"}` for health checks.
