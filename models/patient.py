from models import db
from models.base import BaseModel

class Patient(BaseModel):
    __tablename__ = 'patients'
    protokol = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    complaints = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    blood_pressure = db.Column(db.String(50), nullable=False)
    pulse = db.Column(db.String(50), nullable=False)
    respiratory_rate = db.Column(db.String(50), nullable=False)
    temperature = db.Column(db.String(50), nullable=False)
    saturation = db.Column(db.String(50), nullable=False)
    chronic_diseases = db.Column(db.Text, nullable=True)
    medications = db.Column(db.Text, nullable=True)
    allergy_history = db.Column(db.Text, nullable=True)
    surgical_history = db.Column(db.Text, nullable=True)
    summary = db.Column(db.Text, nullable=True)
    service_coming=db.Column(db.Text, nullable=True)
    triaj = db.Column(db.Text,nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    ip_address = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

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