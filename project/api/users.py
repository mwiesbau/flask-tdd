from flask import Blueprint, request
from flask_restful import Api, Resource
from sqlalchemy import exc

from project import db
from project.api.models import User

users_blueprint = Blueprint("users", __name__)
api = Api(users_blueprint)


class UsersList(Resource):
    def post(self):
        post_data = request.get_json()
        response_object = {"status": "fail", "message": "Invalid payload."}
        if not post_data:
            return response_object, 400
        username = post_data.get("username")
        email = post_data.get("email")
        try:
            user = User.query.filter_by(email=email).first()
            if not user:
                db.session.add(User(username=username, email=email))
                db.session.commit()
                response_object["status"] = "success"
                response_object["message"] = f"{email} was added!"
                return response_object, 201
            else:
                response_object["message"] = "Sorry. That email already exists."
                return response_object, 400
        except exc.IntegrityError:
            db.session.rollback()
            return response_object, 400

    def get(self):
        response_object = {
            "status": "success",
            "data": {"users": [user.to_json() for user in User.query.all()]},
        }

        return response_object, 200


class Users(Resource):
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        response_object = {
            "status": "success",
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "active": user.active,
            },
        }
        return response_object, 200


api.add_resource(Users, "/users/<user_id>")
api.add_resource(UsersList, "/users")
