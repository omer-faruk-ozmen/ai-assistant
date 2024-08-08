from repositories.patient_repository import PatientRepository


patient_repo = PatientRepository()

def get_all_patients_with_relationships_admin():
    return patient_repo.get_all_patients_with_relationships()