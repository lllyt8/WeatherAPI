import requests, os, json
import redis # import redis for caching
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from flask_limiter import Limiter # import Limiter for limiting API requests
from flask_limiter.util import get_remote_address

# 加载环境变量
load_dotenv()

# 使用环境变量，并提供默认值
API_KEY = os.environ.get('WEATHER_API_KEY')
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')

if not API_KEY:
    raise ValueError("WEATHER_API_KEY must be set in environment variables")

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app, 
    default_limits=["100 per hour"]
)
cache = redis.Redis.from_url(REDIS_URL)

CACHE_EXPIRATION = 43200

@app.route('/weather')
@limiter.limit("10 per minute")
def weather():
    city = request.args.get('city', 'New York')
    cache_key = f'weather:{city}'

    # Check if data is in cache
    cache_data = cache.get(cache_key)
    if cache_data:
        return jsonify(json.loads(cache_data))

    # Fetch data from third-party API
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/today/today?key={API_KEY}'
    
    try:
        api_response = requests.get(url)
        api_response.raise_for_status() # Activate exception if status code is not 200
        data = api_response.json()
    except Exception as e:
        return jsonify({"error": "Failed to fetch weather data", "details": str(e)}), 500

    # Save data to cache
    cache.set(cache_key, json.dumps(data), ex=CACHE_EXPIRATION)

    return jsonify(data)

    # response = {
    #     'city': 'New York',
    #     'temperature': 25,
    #     'description': "clear sky"
    # }
    # return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
