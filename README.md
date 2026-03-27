# Hong Kong Weather API

A REST API providing real-time weather data from the Hong Kong Observatory. Built with FastAPI and PostgreSQL, fully containerized with Docker.

## Features
- Real-time temperature, rainfall, and forecast data
- User authentication with secure password hashing
- PostgreSQL database with SQLAlchemy ORM
- Caching system for improved performance

## Tech Stack
- **Backend**: FastAPI, Python 3.11
- **Database**: PostgreSQL with SQLAlchemy
- **Authentication**: PBKDF2 password hashing
- **Containerization**: Docker, Docker Compose

### Prerequisites
- Python 3.11+
- PostgreSQL
- Docker
- Git

### Run with Docker Compose

```bash
# Clone the repository
git clone https://github.com/huishukying/hk-weather-api.git
cd hk-weather-api
docker-compose up -d

# Access the API
Open http://localhost:8000/docs in your browser
