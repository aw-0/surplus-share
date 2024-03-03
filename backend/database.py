import json

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter

cred = credentials.Certificate("secrets/firebase.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()


def get_user(doc_id: str):
    doc_ref = db.collection("users").document(str(doc_id))
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None
    

def get_all_pages(collection):
    users = {}
    doc_ref = db.collection(collection).stream()
    for doc in doc_ref:
        users[doc.id] = doc.to_dict()
    return users
    

def get_all_pages_by_time(collection, time):
    users = get_all_pages(collection)
    for user in list(users):
        if users[user]["time"] != time:
            users.pop(user)
    return users


def save_user(data: dict):
    update_time, user_ref  = db.collection("users").add(data)
    return user_ref.id

def save_biz(data: dict):
    update_time, biz_ref  = db.collection("businesses").add(data)
    return biz_ref.id
