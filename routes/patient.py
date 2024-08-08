# patient_bp.py
from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, jsonify, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import helpers
from utils.decorators import role_required
from services.patient_service import add_patient_result, create_patient, delete_patient_with_relationships, get_patient, get_patient_with_relationships, update_patient, delete_patient, list_patients_by_user_id

patient_bp = Blueprint('patient_bp', __name__)

@patient_bp.route('/add', methods=['POST','GET'])
@jwt_required()
def create_patient_route():
    current_user = get_jwt_identity()
    if request.method == "POST":
        data = {
            'protokol': request.form.get('protokol', 'Belirtilmemiş'),
            'age': request.form.get('age', 'Belirtilmemiş'),
            'gender': request.form.get('gender', 'Belirtilmemiş'),
            'complaints': request.form.get('complaints', 'Belirtilmemiş'),
            'duration': request.form.get('duration', 'Belirtilmemiş'),
            'blood_pressure': request.form.get('bloodPressure', 'Belirtilmemiş'),
            'pulse': request.form.get('pulse', 'Belirtilmemiş'),
            'respiratory_rate': request.form.get('respiratoryRate', 'Belirtilmemiş'),
            'temperature': request.form.get('temperature', 'Belirtilmemiş'),
            'saturation': request.form.get('saturation', 'Belirtilmemiş'),
            'chronic_diseases': request.form.get('chronicDiseases', 'Belirtilmemiş'),
            'medications': request.form.get('medications', 'Belirtilmemiş'),
            'allergy_history': request.form.get('allergyHistory', 'Belirtilmemiş'),
            'surgical_history': request.form.get('surgicalHistory', 'Belirtilmemiş'),
            'summary': request.form.get('summary', 'Belirtilmemiş'),
            'service_coming': request.form.get('service_coming', 'Belirtilmemiş'),
            'triaj': request.form.get('triaj', 'Belirtilmemiş')
        }
        patient = create_patient(
            user_id=current_user['id'],
            data=data,
            date=datetime.now(),
            ip_address=helpers.get_client_ip()
        )
        flash('Hasta başarıyla oluşturuldu.', 'success')
        return redirect(url_for('app_bp.patient_bp.get_patient_route', id=patient.id))
    
    return render_template('patient/add.html')

@patient_bp.route('/edit/<int:id>', methods=['POST', 'GET'])
@jwt_required()
def update_patient_route(id):
    if request.method == 'POST':
        data = {
            'protokol': request.form.get('protokol', 'Belirtilmemiş'),
            'age': request.form.get('age', 'Belirtilmemiş'),
            'gender': request.form.get('gender', 'Belirtilmemiş'),
            'complaints': request.form.get('complaints', 'Belirtilmemiş'),
            'duration': request.form.get('duration', 'Belirtilmemiş'),
            'blood_pressure': request.form.get('bloodPressure', 'Belirtilmemiş'),
            'pulse': request.form.get('pulse', 'Belirtilmemiş'),
            'respiratory_rate': request.form.get('respiratoryRate', 'Belirtilmemiş'),
            'temperature': request.form.get('temperature', 'Belirtilmemiş'),
            'saturation': request.form.get('saturation', 'Belirtilmemiş'),
            'chronic_diseases': request.form.get('chronicDiseases', 'Belirtilmemiş'),
            'medications': request.form.get('medications', 'Belirtilmemiş'),
            'allergy_history': request.form.get('allergyHistory', 'Belirtilmemiş'),
            'surgical_history': request.form.get('surgicalHistory', 'Belirtilmemiş'),
            'summary': request.form.get('summary', 'Belirtilmemiş'),
            'service_coming': request.form.get('service_coming', 'Belirtilmemiş'),
            'triaj': request.form.get('triaj', 'Belirtilmemiş')
        }
        patient = update_patient(id, data)
        if not patient:
            flash('Hasta bulunamadı.', 'danger')
            return redirect(url_for('patient_bp.list_patients'))
        
        flash('Hasta başarıyla güncellendi.', 'success')
        return redirect(url_for('app_bp.patient_bp.get_patient_route', id=patient.id))
    
    patient = get_patient_with_relationships(id)
    if not patient:
        flash('Hasta bulunamadı.', 'danger')
        return redirect(url_for('app_bp.patient_bp.list_patients'))
    
    return render_template('patient/edit.html', patient=patient)

@patient_bp.route('/edit-result/<int:patient_id>', methods=['POST'])
@jwt_required()
def edit_result_route(patient_id):
    result = request.form.get('result')
    if not result:
        flash('Sonuç gerekli.', 'danger')
        return redirect(url_for('app_bp.patient_bp.list_patients_route'))

    conclusion = add_patient_result(patient_id, result)
    if conclusion:
        flash('Sonuç başarıyla eklendi.', 'success')
    else:
        flash('Sonuç eklenirken bir hata oluştu.', 'danger')
    
    return redirect(url_for('app_bp.patient_bp.list_patients_route'))

@patient_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_patient_route(id):
    patient = get_patient_with_relationships(id)
    if not patient:
         flash('Patient not found','warning')
         return render_template('patient')
    return render_template('patient/detail.html',patient=patient)


@patient_bp.route('/delete/<int:id>', methods=['GET','POST'])
@jwt_required()
def delete_patient_route(id):
    success = delete_patient_with_relationships(id)
    if not success:
         flash('Patient not found','warning')
         return redirect(url_for('app_bp.patient_bp.list_patients_route'))
    return redirect(url_for('app_bp.patient_bp.list_patients_route'))

@patient_bp.route('', methods=['GET'])
@jwt_required()
def list_patients_route():
    current_user = get_jwt_identity()
    patients = list_patients_by_user_id(current_user['id'])
    return render_template('patient/list.html', patients=patients)
