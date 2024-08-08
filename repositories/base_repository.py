from models import db
from sqlalchemy.exc import SQLAlchemyError

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def add(self, entity):
        try:
            db.session.add(entity)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def get_all(self):
        return self.model.query.all()

    def get_by_id(self, entity_id):
        return self.model.query.get(entity_id)

    def update(self, entity):
        try:
            db.session.add(entity) 
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def delete(self, entity):
        try:
            db.session.delete(entity)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
