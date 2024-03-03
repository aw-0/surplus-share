from flask import Flask, request, jsonify
import os
from flask_cors import CORS, cross_origin

from helpers import geocode_address, get_distance, create_mega_route, get_all_distances, findBestChild
from database import save_user, save_biz, get_all_pages_by_time, get_all_pages
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/registerUser", methods=["POST", "OPTIONS"])
@cross_origin()
def registerUser():
    data = request.json
    save_user(data)
    #send_sms(data["phone"], "Thank you for registering with SurplusShare! We will contact you soon when your food is near.")
    return jsonify({
        "status": "success"
    })

@app.route("/registerBiz", methods=["POST", "OPTIONS"])
@cross_origin()
def registerBiz():
    data = request.json
    save_biz(data)
    #send_sms(data["phone"], "Thank you for registering with SurplusShare! We will contact you soon with our volunteers are near to pick up your excess food.")
    return jsonify({
        "status": "success"
    })
    
    
@app.route("/getAllUsers", methods=["GET"])
def getAllUsers():
    return jsonify(get_all_pages("users"))

@app.route("/getAllBiz", methods=["GET"])
def getAllBiz():
    return jsonify(get_all_pages("businesses"))

@app.route("/getFoodAmount", methods=["GET"])
def getFoodAmount():
    food_types = ["None", "Halal", "Kosher", "Vegetarian/Vegan", "Gluten Free"]
    
    user_requests = {type: 0 for type in food_types}
    users = get_all_pages("users")
    for key in users.keys():
        user_requests[users[key]["diet"]] += 1
    
    biz_services = {}
    bizs = get_all_pages("businesses")
    for key in bizs.keys():
        biz_services[bizs[key]["diet"]] = int(bizs[key]["foodAmount"])
    
    deliveries = {}
    for type in food_types:
        deliveries[type] = biz_services[type] // user_requests[type]
    
    while (deliveries["Gluten Free"] > deliveries["Halal"] or deliveries["Gluten Free"] > deliveries["Kosher"] or deliveries["Gluten Free"] > deliveries["Vegetarian/Vegan"]):
        if deliveries["Gluten Free"] > deliveries["Halal"]:
            deliveries["Gluten Free"] -= 1
            deliveries["Halal"] += 1
        elif deliveries["Gluten Free"] > deliveries["Kosher"]:
            deliveries["Gluten Free"] -= 1
            deliveries["Kosher"] += 1
        else:
            deliveries["Gluten Free"] -= 1
            deliveries["Vegetarian/Vegan"] += 1
            
    while (deliveries["None"] < deliveries["Halal"] or deliveries["None"] < deliveries["Kosher"] or deliveries["None"] < deliveries["Vegetarian/Vegan"] or deliveries["None"] < deliveries["Gluten Free"]):
        if deliveries["None"] < deliveries["Halal"]:
            deliveries["None"] += 1
            deliveries["Halal"] -= 1
        elif deliveries["None"] < deliveries["Kosher"]:
            deliveries["None"] += 1
            deliveries["Kosher"] -= 1
        elif deliveries["None"] < deliveries["Vegetarian/Vegan"]:
            deliveries["None"] += 1
            deliveries["Vegetarian/Vegan"] -= 1
        else:
            deliveries["None"] += 1
            deliveries["Gluten Free"] -= 1

    return jsonify(deliveries)

    
@app.route("/getUsersRoute", methods=["POST", "OPTIONS"])
@cross_origin()
def getBizRoute():
    data = request.json
    if not data["time"]:
        return jsonify({"error": "No time specified"})
    
    users = get_all_pages_by_time("users", data["time"])
    addresses = [users[key]["address"] + ", " + users[key]["city"] for key in users.keys()]
    for user in users:
        users[user]["longlat"] = geocode_address(users[user]["address"] + ", " + users[user]["city"])
    distances_dict = get_all_distances(addresses)
    if len(distances_dict) <= 2:
        best_child = addresses
        best_child_reconverted = addresses
    else:
        best_child = findBestChild(distances_dict, len(addresses))
        best_child_reconverted = ["1 Stevenson Dr, Lincolnshire"] + [addresses[i] for i in best_child]
    
    return jsonify({"link": create_mega_route(best_child_reconverted), "addresses": best_child_reconverted, "users": users})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
