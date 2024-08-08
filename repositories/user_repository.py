from flask_bcrypt import generate_password_hash
from repositories.base_repository import BaseRepository
from models.user import User

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def get_all_users(self):
        return self.model.query.all()
    
    def update(self, entity):
        super().update(entity)


    def block_user(self, user_id):
        user = self.get_by_id(user_id)
        if user:
            user.is_blocked = True
            self.update(user)
        return user
    
    def unblock_user(self, user_id):
        user = self.get_by_id(user_id)
        if user:
            user.is_blocked = False
            self.update(user)
        return user
    

    def change_password(self, user_id, new_password):
        user = self.get_by_id(user_id)
        if user:
            user.password = generate_password_hash(new_password).decode('utf-8')
            self.update(user)
            return user
        return None