import os

from database import get_all_pages, get_all_pages_by_time, save_biz, save_user
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from helpers import (create_mega_route, findBestChild, geocode_address,
                     get_all_distances, get_distance)

load_dotenv()
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

delivery_info_cache = {}

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
    global delivery_info_cache
    
    food_types = ["None", "Halal", "Kosher", "Vegetarian/Vegan", "Gluten Free"]
    
    user_request_count = {type: 0 for type in food_types}
    users = get_all_pages("users")
    for key in users.keys():
        user_request_count[users[key]["diet"]] += 1
    
    biz_services = {}
    bizs = get_all_pages("businesses")
    for key in bizs.keys():
        biz_services[bizs[key]["diet"]] = int(bizs[key]["foodAmount"])
    
    deliveries_amount = {}
    delivery_info_cache = {}
    for type in food_types:
        deliveries_amount[type] = biz_services[type] // user_request_count[type]
        delivery_info_cache[type] = {type: deliveries_amount[type]}
    print(delivery_info_cache, deliveries_amount, user_request_count)
    
    while (deliveries_amount["Gluten Free"] * user_request_count["Gluten Free"] > deliveries_amount["Halal"] * user_request_count["Halal"] or deliveries_amount["Gluten Free"] * user_request_count["Gluten Free"] > deliveries_amount["Kosher"] * user_request_count["Kosher"] or deliveries_amount["Gluten Free"] * user_request_count["Gluten Free"] > deliveries_amount["Vegetarian/Vegan"] * user_request_count["Vegetarian/Vegan"]):
        print(f"Before: {delivery_info_cache}")
        if deliveries_amount["Gluten Free"] * user_request_count["Gluten Free"] > deliveries_amount["Halal"] * user_request_count["Halal"]:
            deliveries_amount["Gluten Free"] -= user_request_count["Halal"]
            deliveries_amount["Halal"] += user_request_count["Halal"]
            delivery_info_cache["Gluten Free"]["Gluten Free"] -= 1
            if delivery_info_cache["Halal"].get("Gluten Free"):
                delivery_info_cache["Halal"]["Gluten Free"] += 1
            else:
                delivery_info_cache["Halal"]["Gluten Free"] = 1
        elif deliveries_amount["Gluten Free"] * user_request_count["Gluten Free"] > deliveries_amount["Kosher"] * user_request_count["Kosher"]:
            deliveries_amount["Gluten Free"] -= user_request_count["Kosher"]
            deliveries_amount["Kosher"] += user_request_count["Kosher"]
            delivery_info_cache["Gluten Free"]["Gluten Free"] -= 1
            if delivery_info_cache["Kosher"].get("Gluten Free"):
                delivery_info_cache["Kosher"]["Gluten Free"] += 1
            else:
                delivery_info_cache["Kosher"]["Gluten Free"] = 1
        else:
            deliveries_amount["Gluten Free"] -= user_request_count["Vegetarian/Vegan"]
            deliveries_amount["Vegetarian/Vegan"] += user_request_count["Vegetarian/Vegan"]
            delivery_info_cache["Gluten Free"]["Gluten Free"] -= 1
            if delivery_info_cache["Vegetarian/Vegan"].get("Gluten Free"):
                delivery_info_cache["Vegetarian/Vegan"]["Gluten Free"] += 1
            else:
                delivery_info_cache["Vegetarian/Vegan"]["Gluten Free"] = 1
        print(f"After: {delivery_info_cache}")
    while (deliveries_amount["None"] * user_request_count["None"] < deliveries_amount["Halal"] * user_request_count["Halal"] or deliveries_amount["None"] * user_request_count["None"] < deliveries_amount["Kosher"] * user_request_count["Kosher"] or deliveries_amount["None"] * user_request_count["None"] < deliveries_amount["Vegetarian/Vegan"] * user_request_count["Vegetarian/Vegan"] or deliveries_amount["None"] * user_request_count["None"] < deliveries_amount["Gluten Free"] * user_request_count["Gluten Free"]):
        if deliveries_amount["None"] * user_request_count["None"] < deliveries_amount["Halal"] * user_request_count["Halal"]:
            deliveries_amount["None"] += user_request_count["Halal"]
            deliveries_amount["Halal"] -= user_request_count["Halal"]
            delivery_info_cache["Halal"]["Halal"] -= 1
            if delivery_info_cache["None"].get("Halal"):
                delivery_info_cache["None"]["Halal"] += 1
            else:
                delivery_info_cache["None"]["Halal"] = 1
        elif deliveries_amount["None"] * user_request_count["None"] < deliveries_amount["Kosher"] * user_request_count["Kosher"]:
            deliveries_amount["None"] += user_request_count["Kosher"]
            deliveries_amount["Kosher"] -= user_request_count["Kosher"]
            delivery_info_cache["Kosher"]["Kosher"] -= 1
            if delivery_info_cache["None"].get("Kosher"):
                delivery_info_cache["None"]["Kosher"] += 1
            else:
                delivery_info_cache["None"]["Kosher"] = 1
        elif deliveries_amount["None"] * user_request_count["None"] < deliveries_amount["Vegetarian/Vegan"] * user_request_count["Vegetarian/Vegan"]:
            deliveries_amount["None"] += user_request_count["Vegetarian/Vegan"]
            deliveries_amount["Vegetarian/Vegan"] -= user_request_count["Vegetarian/Vegan"]
            delivery_info_cache["Vegetarian/Vegan"]["Vegetarian/Vegan"] -= 1
            if delivery_info_cache["None"].get("Vegetarian/Vegan"):
                delivery_info_cache["None"]["Vegetarian/Vegan"] += 1
            else:
                delivery_info_cache["None"]["Vegetarian/Vegan"] = 1
        else:
            deliveries_amount["None"] += user_request_count["Gluten Free"]
            deliveries_amount["Gluten Free"] -= user_request_count["Gluten Free"]
            delivery_info_cache["Gluten Free"]["Gluten Free"] -= 1
            if delivery_info_cache["None"].get("Gluten Free"):
                delivery_info_cache["None"]["Gluten Free"] += 1
            else:
                delivery_info_cache["None"]["Gluten Free"] = 1

    return jsonify(deliveries_amount)

    
@app.route("/getUsersRoute", methods=["POST", "OPTIONS"])
@cross_origin()
def getBizRoute():
    data = request.json
    if not data["time"]:
        return jsonify({"error": "No time specified"})
    
    users = get_all_pages_by_time("users", data["time"])
    addresses = [users[key]["address"] + ", " + users[key]["city"] for key in users.keys()]
    
    if len(delivery_info_cache) == 0:
        getFoodAmount()
        
    for user in users:
        users[user]["longlat"] = geocode_address(users[user]["address"] + ", " + users[user]["city"])
        users[user]["deliveryInfo"] = delivery_info_cache[users[user]["diet"]]
    distances_dict = get_all_distances(addresses)
    if len(distances_dict) <= 2:
        best_child = addresses
        best_child_reconverted = addresses
    else:
        best_child = findBestChild(distances_dict, len(addresses))
        best_child_reconverted = ["1 Stevenson Dr, Lincolnshire"] + [addresses[i] for i in best_child]
    print(jsonify({"link": create_mega_route(best_child_reconverted), "addresses": best_child_reconverted, "users": users}))
    return jsonify({"link": create_mega_route(best_child_reconverted), "addresses": best_child_reconverted, "users": users})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
