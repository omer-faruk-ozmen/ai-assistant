from models import db
from models.base import BaseModel

class Conclusion(BaseModel):
    __tablename__ = 'conclusions'
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    triage_class = db.Column(db.String(50), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    result = db.Column(db.Text, nullable=True)
