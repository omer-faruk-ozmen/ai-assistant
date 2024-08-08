from models import db
from models.base import BaseModel

class Patient(BaseModel):
    __tablename__ = 'patients'
    protokol = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(15), nullable=True)
    complaints = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(20), nullable=False)
    blood_pressure = db.Column(db.String(10), nullable=True)
    pulse = db.Column(db.String(10), nullable=True)
    respiratory_rate = db.Column(db.String(10), nullable=True)
    temperature = db.Column(db.String(10), nullable=True)
    saturation = db.Column(db.String(10), nullable=True)
    chronic_diseases = db.Column(db.Text, nullable=True)
    medications = db.Column(db.Text, nullable=True)
    allergy_history = db.Column(db.Text, nullable=True)
    surgical_history = db.Column(db.Text, nullable=True)
    summary = db.Column(db.Text, nullable=True)
    service_coming=db.Column(db.Text, nullable=True)
    triaj = db.Column(db.Text,nullable=True)
    date = db.Column(db.DateTime, nullable=True)
    ip_address = db.Column(db.String(50), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'protokol':self.protokol,
            'age': self.age,
            'gender': self.gender,
            'complaints': self.complaints,
            'duration': self.duration,
            'blood_pressure': self.blood_pressure,
            'pulse': self.pulse,
            'respiratory_rate': self.respiratory_rate,
            'temperature': self.temperature,
            'saturation': self.saturation,
            'chronic_diseases': self.chronic_diseases,
            'medications': self.medications,
            'allergy_history': self.allergy_history,
            'surgical_history': self.surgical_history,
            'summary': self.summary,
            'service_coming':self.service_coming,
            'triaj':self.triaj,
            'date': self.date,
            'ip_address': self.ip_address,
            'user_id': self.user_id
        }