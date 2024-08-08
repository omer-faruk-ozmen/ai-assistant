from models import db
from models.base import BaseModel

class Diagnosis(BaseModel):
    __tablename__ = 'diagnosis'
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
