from models.conclusion import Conclusion
from models.diagnosis import Diagnosis
from models.examination import Examination
from models.intervention import Intervention
from models.user import User
from repositories.base_repository import BaseRepository
from models.patient import Patient
from sqlalchemy.exc import SQLAlchemyError

class PatientRepository(BaseRepository):
    def __init__(self):
        super().__init__(Patient)

    def add_patient(self, user_id, **kwargs):
        patient = Patient(user_id=user_id, **kwargs)
        self.add(patient)
        return patient
    
    def add_result(self, patient_id, result):
        patient = self.get_by_id(patient_id)
        if not patient:
            return None
        conclusion = Conclusion.query.filter_by(patient_id=patient_id).first()
        if conclusion:
            conclusion.result = result
            self.update(conclusion)
        else:
            conclusion = Conclusion(patient_id=patient_id, result=result)
            self.add(conclusion)
        return conclusion

    def get_all_relationships(self, patient_id):
        patient = self.get_by_id(patient_id)
        if not patient:
            return None
        
        patient.conclusion = Conclusion.query.filter_by(patient_id=patient_id).first()
        patient.diagnosis = Diagnosis.query.filter_by(patient_id=patient_id).all()
        patient.examination = Examination.query.filter_by(patient_id=patient_id).all()
        patient.intervention = Intervention.query.filter_by(patient_id=patient_id).all()
        
        return patient
    
    def get_all_patients_with_relationships(self):
        patients = self.model.query.order_by(self.model.id.desc()).all()
        for patient in patients:
            patient.user = User.query.filter_by(id=patient.user_id).first()
            patient.conclusion = Conclusion.query.filter_by(patient_id=patient.id).first()
            patient.diagnoses = Diagnosis.query.filter_by(patient_id=patient.id).all()
            patient.examinations = Examination.query.filter_by(patient_id=patient.id).all()
            patient.interventions = Intervention.query.filter_by(patient_id=patient.id).all()

        return patients
    
    def get_all_patients_with_relationships_paginate(self, page, per_page):
        pagination = self.model.query.order_by(self.model.id.desc()).paginate(page=page, per_page=per_page, error_out=False)

        patients = pagination.items
        for patient in patients:
            patient.user = User.query.filter_by(id=patient.user_id).first()
            patient.conclusion = Conclusion.query.filter_by(patient_id=patient.id).first()
            patient.diagnoses = Diagnosis.query.filter_by(patient_id=patient.id).all()
            patient.examinations = Examination.query.filter_by(patient_id=patient.id).all()
            patient.interventions = Intervention.query.filter_by(patient_id=patient.id).all()

        return pagination


    def get_by_user_id(self, user_id):
        patients = self.model.query.filter_by(user_id=user_id).order_by(self.model.id.desc()).all()
        return patients
    
    def get_patient_count_by_user_id(self, user_id):
            return self.model.query.filter_by(user_id=user_id).count()
    
  