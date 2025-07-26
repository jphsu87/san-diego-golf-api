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
    {"name": "Admiral Baker Golf Course", "city": "San Diego", "lat": 32.7927, "lon": -117.1038},
    {"name": "Colina Park Golf Course", "city": "San Diego", "lat": 32.7510, "lon": -117.0835},
    {"name": "Tecolote Canyon Golf Course", "city": "San Diego", "lat": 32.7949, "lon": -117.1882},
    {"name": "Riverwalk Golf Course", "city": "San Diego", "lat": 32.7645, "lon": -117.1704},
    {"name": "Presidio Hills Golf Course", "city": "San Diego", "lat": 32.7560, "lon": -117.1970},
    {"name": "Colina Park Golf Course", "city": "San Diego", "lat": 32.7510, "lon": -117.0835},
    
    {"name": "Coronado Municipal Golf Course", "city": "Coronado", "lat": 32.6848, "lon": -117.1677},
    {"name": "Sea 'N Air Golf Course", "city": "San Diego", "lat": 32.6917, "lon": -117.1954},
    
    {"name": "The Crossings at Carlsbad", "city": "Carlsbad", "lat": 33.1262, "lon": -117.3086},
    {"name": "Encinitas Ranch Golf Course", "city": "Encinitas", "lat": 33.0480, "lon": -117.2610},
    {"name": "Bajamar Golf Resort", "city": "San Diego", "lat": null, "lon": null},  # coords not provided
    {"name": "Aviara Golf Club", "city": "Carlsbad", "lat": 33.0933, "lon": -117.2863},
    {"name": "La Costa North & South", "city": "Carlsbad", "lat": 33.0924, "lon": -117.2658},
    
    {"name": "Oceanside Golf Course", "city": "Oceanside", "lat": 33.2522, "lon": -117.3218},
    {"name": "Emerald Isle Golf Course", "city": "Oceanside", "lat": 33.2153, "lon": -117.3322},
    {"name": "Arrowood Golf Course", "city": "Oceanside", "lat": 33.2744, "lon": -117.2882},
    {"name": "El Camino Country Club", "city": "Oceanside", "lat": 33.1826, "lon": -117.3218},
    {"name": "Goat Hill Park Golf Club", "city": "Oceanside", "lat": null, "lon": null},
    
    {"name": "Carlton Oaks Golf Club", "city": "Santee", "lat": 32.8427, "lon": -117.0097},
    {"name": "Barona Creek Golf Club", "city": "Lakeside", "lat": 32.9335, "lon": -116.8695},
    {"name": "Cottonwood Golf Club", "city": "El Cajon", "lat": 32.7483, "lon": -116.9113},
    {"name": "Maderas Golf Club", "city": "Poway", "lat": 33.0351, "lon": -117.0224},
    
    {"name": "Mt. Woodson Golf Club", "city": "Ramona", "lat": 33.0149, "lon": -116.9556},
    {"name": "Fairbanks Ranch Country Club", "city": "San Diego", "lat": null, "lon": null},
    {"name": "Bernardo Heights Country Club", "city": "San Diego", "lat": 33.0052, "lon": -117.0716},
    {"name": "Morgan Run Resort & Club", "city": "Rancho Santa Fe", "lat": 32.9912, "lon": -117.2093},
    {"name": "Rancho Carlsbad Golf Course", "city": "Carlsbad", "lat": 33.1467, "lon": -117.2893},
    {"name": "Rancho Santa Fe Golf Club", "city": "Rancho Santa Fe", "lat": 33.0248, "lon": -117.2092},
    {"name": "The Crosby National Golf Club", "city": "Rancho Santa Fe", "lat": 33.0210, "lon": -117.1517},
    {"name": "The Bridges at Rancho Santa Fe", "city": "Rancho Santa Fe", "lat": 33.0570, "lon": -117.1886},
    {"name": "The Farms Golf Club", "city": "Rancho Santa Fe", "lat": 32.9858, "lon": -117.1768},
    
    {"name": "Pauma Valley Country Club", "city": "Pauma Valley", "lat": 33.2994, "lon": -116.98895},
    {"name": "Pala Mesa Resort", "city": "Fallbrook", "lat": 33.3556, "lon": -117.1598},
    {"name": "Reidy Creek Golf Course", "city": "Escondido", "lat": 33.1613, "lon": -117.0927},
    {"name": "Eagle Crest Golf Club", "city": "Escondido", "lat": 33.1163, "lon": -117.0074},
    {"name": "Castle Creek Country Club", "city": "Escondido", "lat": 33.2558, "lon": -117.1450},
    {"name": "Vineyard at Escondido", "city": "Escondido", "lat": 33.0732, "lon": -117.0541},
    {"name": "Welk Resorts San Diego", "city": "Escondido", "lat": 33.2325, "lon": -117.1417},
    
    {"name": "Shadowridge Country Club", "city": "Vista", "lat": 33.1682, "lon": -117.2309},
    {"name": "Vista Valley Country Club", "city": "Vista", "lat": 33.2473, "lon": -117.1934},
    {"name": "Twin Oaks Golf Course", "city": "San Marcos", "lat": 33.1669, "lon": -117.1604},
    {"name": "Lake San Marcos Country Club", "city": "San Marcos", "lat": 33.1240, "lon": -117.2040},
    {"name": "St. Mark Golf Club", "city": "San Marcos", "lat": null, "lon": null},
    
    {"name": "San Diego Country Club", "city": "Chula Vista", "lat": null, "lon": null},
    {"name": "Bonita Golf Club", "city": "Bonita", "lat": 32.6801, "lon": -117.0157}
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