from flask import Flask, jsonify
import math
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow all origins (for testing, adjust for production later)

# San Diego golf course data (latitude, longitude, name, city)
courses = [
    {"name": "Torrey Pines South", "city": "San Diego", "lat": 32.9015, "lon": -117.2542},
    {"name": "Torrey Pines North", "city": "San Diego", "lat": 32.8989, "lon": -117.2525},
    {"name": "Balboa Park Golf Course", "city": "San Diego", "lat": 32.7326, "lon": -117.1417},
    {"name": "Mission Bay Golf Course", "city": "San Diego", "lat": 32.7988, "lon": -117.2378},
    {"name": "Encinitas Ranch Golf Course", "city": "San Diego", "lat": 33.0480, "lon": -117.2610}
]

# Haversine formula to calculate distance
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 3958.8  # Earth radius in miles
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

# San Diego coordinates
SAN_DIEGO_LAT, SAN_DIEGO_LON = 32.7157, -117.1611

@app.route('/courses', methods=['GET'])
def get_courses():
    nearby_courses = [
        course for course in courses
        if haversine_distance(SAN_DIEGO_LAT, SAN_DIEGO_LON, course["lat"], course["lon"]) <= 50  # Default 50-mile radius
    ]
    return jsonify({"courses": nearby_courses})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)