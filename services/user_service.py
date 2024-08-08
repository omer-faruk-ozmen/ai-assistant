from flask_jwt_extended import get_jwt_identity
from models.user import User
from repositories.patient_repository import PatientRepository
from repositories.user_repository import UserRepository


user_repo = UserRepository()
patient_repo = PatientRepository()

def get_all_users():
    users= user_repo.get_all_users()

    for user in users:
        user.patient_count = patient_repo.get_patient_count_by_user_id(user.id)
    return users

def update_user_role_service(user_id, role):
    user = user_repo.get_by_id(user_id)
    if user:
        user.role = role
        user_repo.update(user)
        return user
    return None

def block_user(user_id):
    user_repo = UserRepository()
    user = user_repo.block_user(user_id)
    return user

def unblock_user(user_id):
    user_repo = UserRepository()
    user = user_repo.unblock_user(user_id)
    return user

def change_password(user_id, new_password):
    return user_repo.change_password(user_id, new_password)


def get_current_user_service():
    user_id = get_jwt_identity()['id']
    if user_id:
        return User.query.get(user_id)
    return None