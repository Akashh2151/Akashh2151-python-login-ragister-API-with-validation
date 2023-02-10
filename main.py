import pymongo
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from pymongo import MongoClient
import re as r
#_______________________________________________________________
# Making a Connection with MongoClient
client = MongoClient("mongodb://localhost:27017")
# database
db = client["app_database"]
# collection
user = db["User"]
#__________________________________________________________________

app = Flask(__name__)
jwt = JWTManager(app)
# JWT Config
app.config["JWT_SECRET_KEY"] = "this-is-secret-key"




@app.route("/dashboard")
@jwt_required
def dasboard():
    return jsonify(message="Welcome! to our task kiran")







@app.route("/register", methods=["POST"])
def register():
    email = (request.form.get("email"))
    password = (request.form.get("password"))
    # pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    
    # email validation 
    regexp = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # strong password validation 
    regexx = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    # print("ha email aahe___________ ",email)

    # print("_____________ check kya he ")
    

    # a=0
    # y=len(email)
    # dot=email.find(".")
    # at=email.find("@")

    # for i in range (0,at):
    #     if((email[i]>='a' and email[i]<='z') or (email[i]>='A' and email[i]<='Z')):
    #         a=a+1
    # if(a>0 and at>0 and (dot-at)>0 and (dot+1)<y):
    #     print("Valid Email")
    # else:
    #     print("Invalid Email")


    # test = User.query.filter_by(email=email).first()

    test = user.find_one({"email": email})
    print(f"test_____________________________________{test}")

    if test:
        return jsonify(message="email id is alredy exist "), 409 

    if r.fullmatch(regexp, email) and r.fullmatch(regexx,password):
        first_name = (request.form.get("first_name"))
        print(f"name fst________________________________________{first_name}")
        last_name = (request.form.get("last_name"))
        print(f"lastname_________________________________________________________________{last_name}")
       
        # password = (request.form.get("password"))
        # print(f"password_________________________________________________{password}")
        user_info = dict(first_name=first_name, last_name=last_name, email=email, password=password)
        print(f"all info_____________________________________________________________{user_info}")
        user.insert_one(user_info)
        return jsonify(message="User added sucessfully"), 201
    
  
    else:   

        return jsonify(message="check your email id and password formate"),409     
        









@app.route("/login", methods=["POST"])
def login():
    if request.is_json:
        email = request.json["email"]
        password = request.json["password"]
    else:
        email = request.form["email"]
        password = request.form["password"]

    test = user.find_one({"email": email, "password": password})
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login Succeeded!", access_token=access_token), 201
    else:
        return jsonify(message="Bad Email or Password"), 401


if __name__ == '__main__':
    app.run(host="localhost", debug=True)