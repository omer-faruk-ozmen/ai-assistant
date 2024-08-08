# repositories/examination_repository.py
from models import Examination
from repositories.base_repository import BaseRepository

class ExaminationRepository(BaseRepository):
    def __init__(self):
        super().__init__(Examination)

    def add_examination(self, patient_id, examination):
        examination_instance = Examination(patient_id=patient_id, examination=examination)
        self.add(examination_instance)
        return examination_instance

    def get_by_patient_id(self, patient_id):
        return self.model.query.filter_by(patient_id=patient_id).all()

    def delete_by_patient_id(self, patient_id):
        return self.model.query.filter_by(patient_id=patient_id).delete()