# Weather API Service

A Flask-based Weather API service with Redis caching and rate limiting.

## Features
- Weather data from Visual Crossing API
- Redis caching
- Rate limiting
- Environment variable configuration

## Setup
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your API key:
   ```bash
   cp .env.example .env
   ```
4. Run the server:
   ```bash
   python weatherAPI.py
   ```

## API Usage
```bash
curl "http://localhost:5000/weather?city=Beijing"
```

## Environment Variables
- `WEATHER_API_KEY`: Your Visual Crossing API key
- `REDIS_URL`: Redis connection URL (default: redis://localhost:6379)