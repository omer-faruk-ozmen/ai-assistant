# repositories/diagnosis_repository.py
from models import Diagnosis
from repositories.base_repository import BaseRepository

class DiagnosisRepository(BaseRepository):
    def __init__(self):
        super().__init__(Diagnosis)

    def add_diagnosis(self, patient_id, diagnosis):
        diagnosis_instance = Diagnosis(patient_id=patient_id, diagnosis=diagnosis)
        self.add(diagnosis_instance)
        return diagnosis_instance

    def get_by_patient_id(self, patient_id):
        return self.model.query.filter_by(patient_id=patient_id).all()

    def delete_by_patient_id(self, patient_id):
        return self.model.query.filter_by(patient_id=patient_id).delete()