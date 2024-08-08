# repositories/conclusion_repository.py
from models import Conclusion
from repositories.base_repository import BaseRepository

class ConclusionRepository(BaseRepository):
    def __init__(self):
        super().__init__(Conclusion)

    def add_conclusion(self, patient_id, triage_class, prompt, result):
        conclusion = Conclusion(
            patient_id=patient_id,
            triage_class=triage_class,
            prompt=prompt,
            result=result
        )
        self.add(conclusion)
        return conclusion

    def get_by_patient_id(self, patient_id):
        return self.model.query.filter_by(patient_id=patient_id).first()

    def delete_by_patient_id(self, patient_id):
        return self.model.query.filter_by(patient_id=patient_id).delete()
        
     