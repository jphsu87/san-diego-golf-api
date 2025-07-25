from flask import Flask, jsonify
import math
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow all origins (for testing, adjust for production later)

# San Diego golf course data (latitude, longitude, name, city)
courses = [
    {"name": "3‑Par At Four Points", "city": "San Diego", "lat": 32.810005, "lon": -117.15043},
    {"name": "Admiral Baker Golf Course", "city": "San Diego", "lat": 32.792723, "lon": -117.103797},
    {"name": "Arrowood Golf Course", "city": "Oceanside", "lat": 33.274351, "lon": -117.288241},
    {"name": "Balboa Park Golf Course", "city": "San Diego", "lat": 32.724447, "lon": -117.136691},
    {"name": "Barona Creek Golf Club", "city": "Lakeside", "lat": 32.933515, "lon": -116.869462},
    {"name": "Bernardo Heights Country Club", "city": "San Diego", "lat": 33.005189, "lon": -117.071567},
    {"name": "Bonita Golf Club", "city": "Bonita", "lat": 32.680119, "lon": -117.015699},
    {"name": "Borrego Springs Resort & Country Club", "city": "Borrego Springs", "lat": 33.235901, "lon": -116.357429},
    {"name": "Carlton Oaks Country Club", "city": "Santee", "lat": 32.842719, "lon": -117.009671},
    {"name": "Carmel Mountain Ranch Country Club", "city": "San Diego", "lat": 32.974784, "lon": -117.076317},
    {"name": "Castle Creek Country Club", "city": "Escondido", "lat": 33.25575, "lon": -117.145014},
    {"name": "Center City Golf Course", "city": "Oceanside", "lat": 33.197462, "lon": -117.358265},
    {"name": "Chula Vista Municipal Golf Course", "city": "Bonita", "lat": 32.661286, "lon": -117.031867},
    {"name": "Colina Park Golf Course", "city": "San Diego", "lat": 32.75104, "lon": -117.083535},
    {"name": "Coronado Municipal Golf Course", "city": "Coronado", "lat": 32.684808, "lon": -117.167659},
    {"name": "Cottonwood Golf Club", "city": "El Cajon", "lat": 32.748314, "lon": -116.91134},
    {"name": "De Anza Desert Country Club", "city": "Borrego Springs", "lat": 33.290496, "lon": -116.384463},
    {"name": "Del Mar Country Club", "city": "Rancho Santa Fe", "lat": 32.978568, "lon": -117.195727},
    {"name": "Doubletree Golf Resort", "city": "San Diego", "lat": 32.978265, "lon": -117.091142},
    {"name": "Eagle Crest Golf Club", "city": "Escondido", "lat": 33.116285, "lon": -117.007417},
    {"name": "Eastlake Country Club", "city": "Chula Vista", "lat": 32.639487, "lon": -116.958181},
    {"name": "El Camino Country Club", "city": "Oceanside", "lat": 33.182594, "lon": -117.321822},
    {"name": "Emerald Isle Golf Course", "city": "Oceanside", "lat": 33.215256, "lon": -117.332191},
    {"name": "Encinitas Ranch Golf Course", "city": "Encinitas", "lat": 33.068324, "lon": -117.275501},
    {"name": "Escondido Country Club", "city": "Escondido", "lat": 33.157101, "lon": -117.124232},
    {"name": "Fairbanks Ranch Country Club", "city": "Rancho Santa Fe", "lat": 32.9791, "lon": -117.206819},
    {"name": "Fallbrook Golf Club", "city": "Fallbrook", "lat": 33.342525, "lon": -117.190623},
    {"name": "Four Seasons Resort Aviara", "city": "Carlsbad", "lat": 33.093277, "lon": -117.286309},
    {"name": "La Costa Resort & Spa", "city": "Carlsbad", "lat": 33.092411, "lon": -117.265783},
    {"name": "La Jolla Beach & Tennis Club", "city": "La Jolla", "lat": 32.852141, "lon": -117.260794},
    {"name": "La Jolla Country Club", "city": "La Jolla", "lat": 32.837455, "lon": -117.269581},
    {"name": "Lake San Marcos Country Club", "city": "San Marcos", "lat": 33.124022, "lon": -117.203977},
    {"name": "Lake San Marcos Executive Golf Course", "city": "San Marcos", "lat": 33.121423, "lon": -117.21745},
    {"name": "Lomas Santa Fe Country Club", "city": "Solana Beach", "lat": 32.995834, "lon": -117.240739},
    {"name": "Lomas Santa Fe Executive Golf Course", "city": "Solana Beach", "lat": 32.999456, "lon": -117.239646},
    {"name": "Maderas Golf Club", "city": "Poway", "lat": 33.035097, "lon": -117.022409},
    {"name": "Marine Memorial Golf Course", "city": "Camp Pendleton", "lat": 33.26824, "lon": -117.328267},
    {"name": "Meadow Lake Golf Course", "city": "Escondido", "lat": 33.215505, "lon": -117.109291},
    {"name": "Miramar Memorial Golf Course", "city": "San Diego", "lat": 32.885722, "lon": -117.138227},
    {"name": "Mission Bay Golf Resort", "city": "San Diego", "lat": 32.798836, "lon": -117.216405},
    {"name": "Mission Trails Golf Course", "city": "San Diego", "lat": 32.8015, "lon": -117.037732},
    {"name": "Montesoro Golf and Social Club", "city": "Borrego Springs", "lat": 33.193965, "lon": -116.323788},
    {"name": "Morgan Run Resort & Club", "city": "Rancho Santa Fe", "lat": 32.991195, "lon": -117.209306},
    {"name": "Mt. Woodson Country Club", "city": "Ramona", "lat": 33.01485, "lon": -116.955599},
    {"name": "National City Golf Course", "city": "National City", "lat": 32.661119, "lon": -117.084296},
    {"name": "Oaks North Executive Golf Course", "city": "San Diego", "lat": 33.032937, "lon": -117.057673},
    {"name": "Ocean Hills Country Club", "city": "Oceanside", "lat": 33.162386, "lon": -117.267852},
    {"name": "Oceanside Golf Course", "city": "Oceanside", "lat": 33.25218, "lon": -117.32179},
    {"name": "Pala Mesa Resort", "city": "Fallbrook", "lat": 33.355594, "lon": -117.159798},
    {"name": "Palacio Del Mar Golf Course", "city": "San Diego", "lat": 32.941935, "lon": -117.212359},
    {"name": "Pauma Valley Country Club", "city": "Pauma Valley", "lat": 33.299437, "lon": -116.988951},
    {"name": "Presidio Hills Golf Course", "city": "San Diego", "lat": 32.756011, "lon": -117.197025},
    {"name": "Rancho Bernardo Inn Golf Course", "city": "San Diego", "lat": 33.029698, "lon": -117.06698},
    {"name": "Rancho Carlsbad Golf Course", "city": "Carlsbad", "lat": 33.146683, "lon": -117.289256},
    {"name": "Rancho Monserate Country Club", "city": "Fallbrook", "lat": 33.31737, "lon": -117.163757},
    {"name": "Rancho Santa Fe Golf Club", "city": "Rancho Santa Fe", "lat": 33.024761, "lon": -117.209233},
    {"name": "Reidy Creek Golf Course", "city": "Escondido", "lat": 33.161259, "lon": -117.092674},
    {"name": "Riverwalk Golf Club", "city": "San Diego", "lat": 32.76453, "lon": -117.170399},
    {"name": "Road Runner Golf & Country Club", "city": "Borrego Springs", "lat": 33.256848, "lon": -116.360751},
    {"name": "Sail Ho Golf Club", "city": "San Diego", "lat": 32.742563, "lon": -117.210367},
    {"name": "San Diego Country Club", "city": "Chula Vista", "lat": 32.623277, "lon": -117.062201},
    {"name": "San Luis Rey Downs Golf Resort", "city": "Bonsall", "lat": 33.28645, "lon": -117.213364},
    {"name": "San Vicente Inn & Golf Club", "city": "Ramona", "lat": 33.002681, "lon": -116.807212},
    {"name": "Sea 'N Air Golf Course", "city": "San Diego", "lat": 32.691736, "lon": -117.195383},
    {"name": "Shadowridge Country Club", "city": "Vista", "lat": 33.168235, "lon": -117.230861},
    {"name": "Skyline Ranch Country Club", "city": "Valley Center", "lat": 33.207229, "lon": -116.949513},
    {"name": "Springs At Borrego Golf Course", "city": "Borrego Springs", "lat": 33.264791, "lon": -116.365958},
    {"name": "Steele Canyon Golf Club", "city": "Jamul", "lat": 32.743198, "lon": -116.894093},
    {"name": "StoneRidge Country Club", "city": "Poway", "lat": 33.021939, "lon": -117.038598},
    {"name": "Sun Valley Fairways", "city": "La Mesa", "lat": 32.770602, "lon": -117.016036},
    {"name": "Sycuan Resort", "city": "El Cajon", "lat": 32.786443, "lon": -116.884866},
    {"name": "Tecolote Canyon Golf Course", "city": "San Diego", "lat": 32.794943, "lon": -117.188217},
    {"name": "The Auld Course", "city": "Chula Vista", "lat": 32.664838, "lon": -116.95558},
    {"name": "The Bridges At Rancho Santa Fe", "city": "Rancho Santa Fe", "lat": 33.056989, "lon": -117.188646},
    {"name": "The Country Club of Rancho Bernardo", "city": "San Diego", "lat": 33.031087, "lon": -117.063569},
    {"name": "The Crosby National Golf Club", "city": "San Diego", "lat": 33.021038, "lon": -117.151706},
    {"name": "The Crossings at Carlsbad", "city": "Carlsbad", "lat": 33.126198, "lon": -117.308598},
    {"name": "The Farms Golf Club", "city": "Rancho Santa Fe", "lat": 32.985793, "lon": -117.176845},
    {"name": "The Golf Club of California", "city": "Fallbrook", "lat": 33.32132, "lon": -117.201627},
    {"name": "The Grand Golf Club", "city": "San Diego", "lat": 32.939214, "lon": -117.197446},
    {"name": "The Santaluz Club", "city": "San Diego", "lat": 32.992881, "lon": -117.148278},
    {"name": "Torrey Pines Golf Course", "city": "La Jolla", "lat": 32.9045, "lon": -117.2454},
    {"name": "Town Park Villas Golf Course", "city": "San Diego", "lat": 32.851254, "lon": -117.19095},
    {"name": "Twin Oaks Golf Course", "city": "San Marcos", "lat": 33.166897, "lon": -117.16044},
    {"name": "Vineyard At Escondido", "city": "Escondido", "lat": 33.073165, "lon": -117.054074},
    {"name": "Vista Valley Country Club", "city": "Vista", "lat": 33.247343, "lon": -117.193445},
    {"name": "Welk Resort San Diego", "city": "Escondido", "lat": 33.232512, "lon": -117.141708},
    {"name": "Willowbrook Golf Course", "city": "Lakeside", "lat": 32.864011, "lon": -116.938316},
    {"name": "Woods Valley Golf Club", "city": "Valley Center", "lat": 33.205258, "lon": -117.014086}
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