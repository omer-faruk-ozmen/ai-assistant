from models import db
from models.base import BaseModel

class Intervention(BaseModel):
    __tablename__ = 'interventions'
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    intervention = db.Column(db.Text, nullable=False)
