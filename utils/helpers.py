
from datetime import datetime
from io import BytesIO
import os
import time
from typing import Any, Dict
from dotenv import load_dotenv
from flask import json, request
from concurrent.futures import  ThreadPoolExecutor, as_completed
from flask_jwt_extended import get_jwt_identity
import pandas as pd
from openai import OpenAI
from models.conclusion import Conclusion
from models.diagnosis import Diagnosis
from models.examination import Examination
from models.intervention import Intervention
from models.user import User
from repositories.conclusion_repository import ConclusionRepository
from repositories.diagnosis_repository import DiagnosisRepository
from repositories.examination_repository import ExaminationRepository
from repositories.intervention_repository import InterventionRepository
from repositories.request_repository import RequestRepository
from services.api_service import ApiService

load_dotenv()
assistant_id = os.environ.get('OPENAI_ASSISTANT_ID')

conclusion_repo = ConclusionRepository()
diagnosis_repo = DiagnosisRepository()
examination_repo = ExaminationRepository()
intervention_repo = InterventionRepository()

thread_ids=[]

def get_client_ip():
    return request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ['REMOTE_ADDR']

def get_current_user():
    user_identity = get_jwt_identity()
    if user_identity:
        return User.query.get(user_identity['id'])
    return 'Unknown'
def create_prompt(patient):
    prompt = "Patient information:"

    if patient.age:
        prompt += f" Age: {patient.age},"
    if patient.gender:
        prompt += f" Gender: {patient.gender},"
    if patient.complaints:
        prompt += f" Complaints: {patient.complaints},"
    if patient.duration:
        prompt += f" Duration of complaint: {patient.duration},"
    if patient.blood_pressure:
        prompt += f" Vital signs: Blood pressure {patient.blood_pressure} mmHg,"
    if patient.pulse:
        prompt += f" Pulse {patient.pulse} bpm,"
    if patient.respiratory_rate:
        prompt += f" Respiratory rate {patient.respiratory_rate} breaths/minute,"
    if patient.temperature:
        prompt += f" Temperature {patient.temperature} °C,"
    if patient.saturation:
        prompt += f" Saturation %{patient.saturation},"
    if patient.chronic_diseases:
        prompt += f" Chronic diseases: {patient.chronic_diseases},"
    if patient.medications:
        prompt += f" Medications in use: {patient.medications},"
    if patient.allergy_history:
        prompt += f" Allergy history: {patient.allergy_history},"
    if patient.surgical_history:
        prompt += f" Surgical history: {patient.surgical_history},"
    if patient.summary:
        prompt += f" Short summary of complaint in patient's own words: \"{patient.summary}\","
    if patient.service_coming:
        prompt += f" Type of Emergency service coming: {patient.service_coming}"

    
    return prompt


base_url = "https://api.openai.com"
headers = {
    "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}",
    "Content-Type": "application/json",
    "OpenAI-Beta":"assistants=v2"
}

repository = RequestRepository(base_url, headers)
api_service = ApiService(repository)

executor = ThreadPoolExecutor(max_workers=10)

def generate_with_ai( prompt: str) -> Dict[str, Any]:
    create_response = api_service.create_thread(assistant_id, prompt)
    thread_id = create_response['thread_id']
    run_id = create_response['id']

    thread_ids.append(thread_id)

    if len(thread_ids)>20:
        oldest_thread_id = thread_ids.pop(0)
        delete_thread(oldest_thread_id)

    future = executor.submit(check_thread_status, thread_id, run_id)
    messages_response = future.result()
    
    return messages_response

def delete_thread(thread_id):
    response = api_service.delete_thread(thread_id)
    return response

def check_thread_status(thread_id: str, run_id: str) -> Dict[str, Any]:
    while True:
        status_response = api_service.get_thread_status(thread_id, run_id)
        if status_response['status'] == 'completed':
            messages_response = api_service.get_thread_messages(thread_id)
            return messages_response
        time.sleep(1)

def proccess_data(data):
    for message in data['data']:
        if message['role'] == 'assistant':
            content = message['content'][0]['text']['value']
            try:
                json_content = json.loads(content)
                return json_content
            except KeyError as e:
                print(f"KeyError: {e}")
            except json.JSONDecodeError as e:
                print(f"JSONDecodeError: {e}")

def process_patient_dict_data(patient_id,response,prompt):

    data = proccess_data(response)

    triage_class = data['triage_class']
    
    conclusion_repo.add(Conclusion(patient_id=patient_id,triage_class=triage_class,prompt=prompt))
    
    for diag in data['pre_diag']:
        diagnosis_repo.add(Diagnosis(patient_id=patient_id,diagnosis=diag))
    
    for exam in data['examination']:
        examination_repo.add(Examination(patient_id=patient_id, examination=exam))

    for treatment in data['treatment']:
        intervention_repo.add(Intervention(patient_id=patient_id, intervention=treatment))


def generate_excel(patients):
    data = []
    for patient in patients:
        conclusion_result = patient.conclusion.result if patient.conclusion else "Sonuç Yok"
        diagnoses = "; ".join([d.diagnosis for d in patient.diagnoses])
        examinations = "; ".join([e.examination for e in patient.examinations])
        interventions = "; ".join([i.intervention for i in patient.interventions])


        data.append({
            "Protokol": patient.protokol,
            "Tarih": patient.date,
            "Kullanıcı": patient.user.username if patient.user else "Bilinmiyor",
            "IP Adresi": patient.ip_address,
            "Triaj": patient.triaj,
            "Yapay Zeka Triaj": patient.conclusion.triage_class if patient.conclusion else "YOK",
            "Yaş": patient.age,
            "Cinsiyet": patient.gender,
            "Şikayet": patient.complaints,
            "Süre": patient.duration,
            "Kan Basıncı": patient.blood_pressure,
            "Nabız": patient.pulse,
            "Solunum Hızı": patient.respiratory_rate,
            "Sıcaklık": patient.temperature,
            "Saturasyon": patient.saturation,
            "Kronik Hastalıklar": patient.chronic_diseases,
            "İlaçlar": patient.medications,
            "Alerji Geçmişi": patient.allergy_history,
            "Cerrahi Geçmiş": patient.surgical_history,
            "Özet": patient.summary,
            "Geliş Tipi":patient.service_coming,
            "Sonuç": conclusion_result,
            "Tanılar": diagnoses,
            "Tetkikler": examinations,
            "Müdahaleler": interventions
        })

    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Patients')
    output.seek(0)
    return output