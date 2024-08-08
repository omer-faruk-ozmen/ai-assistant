from models import db
from models.base import BaseModel

class Examination(BaseModel):
    __tablename__ = 'examinations'
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    examination = db.Column(db.Text, nullable=False)
