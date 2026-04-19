# Hong Kong Weather API

A FastAPI-based REST API providing real-time weather data from the Hong Kong Observatory (HKO), featuring user authentication, database storage, and Docker containerization.

## Features
- **Real-time Weather Data** - Temperature, rainfall, and 9-day forecast from (HKO)
- **JWT Authentication** - Secure user registration and login with PBKDF2 password hashing
- **PostgreSQL Database** - User management with SQLAlchemy ORM
- **Caching System** - 5-minute in-memory cache to reduce external API calls
- **Docker Support**

## Tech Stack
- **FastAPI**
- **PostgreSQL**
- **JWT + PBKDF2**
- **Docker**

## Quick Start with Docker
Pre-built image available on [Docker Hub](https://hub.docker.com/r/huishukying/hk-weather-api)

### Run the Application
```bash
# 1. Clone the repository
git clone https://github.com/huishukying/hk-weather-api.git
cd hk-weather-api


# 2. Create .env file with your JWT secret
echo 'JWT_SECRET_KEY=your-super-secret-key-here' > .env

# 3. Start the application
docker-compose up --build
