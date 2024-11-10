# Airline Management API

This is a REST API for managing airlines and their aircraft. The API provides endpoints for creating, reading, updating, and deleting airlines and aircraft data.

## Prerequisites

- Python 3.x
- pip (Python package installer)
- virtualenv (recommended)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd <project-directory>
```

2. Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv env

# Activate virtual environment
# For Windows:
.\env\Scripts\activate
# For macOS/Linux:
source env/bin/activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Apply database migrations:

```bash
python manage.py migrate
```

The migration will automatically create a default superuser:

- Username: user
- Password: 1234

## Running the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Authentication

- `POST /api-token-auth/`: Obtain authentication token

### Airlines

- `GET /airline/`: List all airlines
- `POST /airline/`: Create a new airline
- `GET /airline/{id}/`: Retrieve a specific airline
- `PATCH /airline/{id}/`: Update a specific airline
- `DELETE /airline/{id}/`: Delete a specific airline

### Aircraft

- `POST /aircraft/`: Create a new aircraft
- `GET /aircraft/{id}/`: Retrieve a specific aircraft
- `PATCH /aircraft/{id}/`: Update a specific aircraft
- `DELETE /aircraft/{id}/`: Delete a specific aircraft

## API Usage

All requests (except authentication) require a JWT token in the header:

```
Authorization: Token <your-token>
```
