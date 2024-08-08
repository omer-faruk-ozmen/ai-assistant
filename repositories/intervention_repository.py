# repositories/intervention_repository.py
from models import Intervention
from repositories.base_repository import BaseRepository

class InterventionRepository(BaseRepository):
    def __init__(self):
        super().__init__(Intervention)

    def add_intervention(self, patient_id, intervention):
        intervention_instance = Intervention(patient_id=patient_id, intervention=intervention)
        self.add(intervention_instance)
        return intervention_instance

    def get_by_patient_id(self, patient_id):
        return self.model.query.filter_by(patient_id=patient_id).all()
    
    def delete_by_patient_id(self, patient_id):
        return self.model.query.filter_by(patient_id=patient_id).delete()