# patient_service.py
import datetime
import logging
from models import db, Patient
from models.conclusion import Conclusion
from models.diagnosis import Diagnosis
from models.examination import Examination
from models.intervention import Intervention
from repositories.conclusion_repository import ConclusionRepository
from repositories.diagnosis_repository import DiagnosisRepository
from repositories.examination_repository import ExaminationRepository
from repositories.intervention_repository import InterventionRepository
from repositories.patient_repository import PatientRepository
from utils import helpers

patient_repo = PatientRepository()
conclusion_repo = ConclusionRepository()
diagnosis_repo = DiagnosisRepository()
examination_repo = ExaminationRepository()
intervention_repo = InterventionRepository()

_logger = logging.getLogger('app')

def create_patient(user_id, data, date, ip_address):
    patient = patient_repo.add_patient(
        user_id=user_id,
        protokol = data.get('protokol'),
        age=data.get('age'),
        gender=data.get('gender'),
        complaints=data.get('complaints'),
        duration=data.get('duration'),
        blood_pressure=data.get('blood_pressure'),
        pulse=data.get('pulse'),
        respiratory_rate=data.get('respiratory_rate'),
        temperature=data.get('temperature'),
        saturation=data.get('saturation'),
        chronic_diseases=data.get('chronic_diseases'),
        medications=data.get('medications'),
        allergy_history=data.get('allergy_history'),
        surgical_history=data.get('surgical_history'),
        summary=data.get('summary'),
        service_coming=data.get('service_coming'),
        triaj = data.get('triaj'),
        date=date,
        ip_address=ip_address
    )

    prompt = helpers.create_prompt(patient=patient)
    response = helpers.generate_with_ai(prompt)
    helpers.process_patient_dict_data(patient_id=patient.id, response=response, prompt=prompt)
    return patient

def update_patient(patient_id, data):
    patient = patient_repo.get_by_id(patient_id)
    if not patient:
        return None

    patient.protokol = data.get('protokol',patient.protokol)
    patient.age = data.get('age', patient.age)
    patient.gender = data.get('gender', patient.gender)
    patient.complaints = data.get('complaints', patient.complaints)
    patient.duration = data.get('duration', patient.duration)
    patient.blood_pressure = data.get('blood_pressure', patient.blood_pressure)
    patient.pulse = data.get('pulse', patient.pulse)
    patient.respiratory_rate = data.get('respiratory_rate', patient.respiratory_rate)
    patient.temperature = data.get('temperature', patient.temperature)
    patient.saturation = data.get('saturation', patient.saturation)
    patient.chronic_diseases = data.get('chronic_diseases', patient.chronic_diseases)
    patient.medications = data.get('medications', patient.medications)
    patient.allergy_history = data.get('allergy_history', patient.allergy_history)
    patient.surgical_history = data.get('surgical_history', patient.surgical_history)
    patient.summary = data.get('summary', patient.summary),
    patient.service_coming=data.get('service_coming',patient.service_coming),
    patient.triaj = data.get('triaj',patient.triaj)

    patient_repo.update(patient)

    conclusion_repo.delete_by_patient_id(patient_id)
    diagnosis_repo.delete_by_patient_id(patient_id)
    examination_repo.delete_by_patient_id(patient_id)
    intervention_repo.delete_by_patient_id(patient_id)

    prompt = helpers.create_prompt(patient=patient)
    response = helpers.generate_with_ai(prompt=prompt)

    helpers.process_patient_dict_data(patient_id=patient.id, response=response, prompt=prompt)

    return patient

def add_patient_result(patient_id, result):
    patient = patient_repo.add_result(patient_id, result)
    if not patient:
        return None, "Patient not found"
    return patient, None

def get_patient(id):
    return patient_repo.get_by_id(id)


def delete_patient(id):
    patient = patient_repo.get_by_id(id)
    if not patient:
        return False

    patient_repo.delete(patient)
    
    return True

def list_patients_by_user_id(user_id):
    patients = patient_repo.get_by_user_id(user_id)
    for patient in patients:
        patient.conclusion=patient.conclusion = Conclusion.query.filter_by(patient_id=patient.id).first()
    
    return patients

def get_patient_with_relationships(patient_id):
    return patient_repo.get_all_relationships(patient_id)


def delete_patient_with_relationships(patient_id):
    conclusions = Conclusion.query.filter_by(patient_id=patient_id).all()
    for conclusion in conclusions:
        conclusion_repo.delete(conclusion)
    
    diagnoses = Diagnosis.query.filter_by(patient_id=patient_id).all()
    for diagnosis in diagnoses:
        diagnosis_repo.delete(diagnosis)
    
    examinations = Examination.query.filter_by(patient_id=patient_id).all()
    for examination in examinations:
        examination_repo.delete(examination)
    
    interventions = Intervention.query.filter_by(patient_id=patient_id).all()
    for intervention in interventions:
        intervention_repo.delete(intervention)
    
    patient = patient_repo.get_by_id(patient_id)
    if patient:
        patient_repo.delete(patient)
        return True
    return False

def get_patients_by_user_id(user_id):
    patient_repo = PatientRepository()
    return patient_repo.get_by_user_id(user_id)

