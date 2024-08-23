from repositories.patient_repository import PatientRepository


patient_repo = PatientRepository()

def get_all_patients_with_relationships_admin():
    return patient_repo.get_all_patients_with_relationships()


def get_all_patients_with_relationships_paginate_admin(page,per_page):
    return patient_repo.get_all_patients_with_relationships_paginate(page,per_page)