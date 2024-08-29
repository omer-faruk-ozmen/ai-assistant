from datetime import datetime
import logging
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import helpers
from services.patient_service import add_patient_result, create_patient, delete_patient_with_relationships, get_patient_with_relationships, update_patient, list_patients_by_user_id

logger = logging.getLogger('app')

patient_bp = Blueprint('patient_bp', __name__)

@patient_bp.route('/add', methods=['POST','GET'])
@jwt_required()
def create_patient_route():
    current_user = get_jwt_identity()
    logger.info(f"User {current_user['username']} accessed create patient route.")
    if request.method == "POST":
        logger.info(f"User {current_user['username']} is attempting to create a new patient.")
        try:
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
            logger.info(f"Patient created successfully with ID: {patient.id} by user {current_user['username']}.")
            flash('Hasta başarıyla oluşturuldu.', 'success')
            return redirect(url_for('app_bp.patient_bp.get_patient_route', id=patient.id))
        except Exception as e:
            logger.error(f"Error creating patient for user {current_user['username']}: {e}")
            flash('Hasta oluşturulurken bir hata oluştu.', 'danger')
            return redirect(url_for('app_bp.patient_bp.create_patient_route'))
    
    return render_template('patient/add.html')

@patient_bp.route('/edit/<int:id>', methods=['POST', 'GET'])
@jwt_required()
def update_patient_route(id):
    current_user = get_jwt_identity()
    logger.info(f"User {current_user['username']} accessed update patient route for patient ID: {id}.")
    
    if request.method == 'POST':
        logger.info(f"User {current_user['username']} is attempting to update patient with ID: {id}.")
        try:
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
                logger.warning(f"Patient with ID {id} not found for user {current_user['username']}.")
                flash('Hasta bulunamadı.', 'danger')
                return redirect(url_for('patient_bp.list_patients'))
            
            logger.info(f"Patient with ID {id} updated successfully by user {current_user['username']}.")
            flash('Hasta başarıyla güncellendi.', 'success')
            return redirect(url_for('app_bp.patient_bp.get_patient_route', id=patient.id))
        except Exception as e:
            logger.error(f"Error updating patient with ID {id} for user {current_user['username']}: {e}")
            flash('Hasta güncellenirken bir hata oluştu.', 'danger')
            return redirect(url_for('app_bp.patient_bp.update_patient_route', id=id))
    
    patient = get_patient_with_relationships(id)
    if not patient:
        logger.warning(f"Patient with ID {id} not found for user {current_user['username']} while accessing edit page.")
        flash('Hasta bulunamadı.', 'danger')
        return redirect(url_for('app_bp.patient_bp.list_patients'))
    
    return render_template('patient/edit.html', patient=patient)

@patient_bp.route('/edit-result/<int:patient_id>', methods=['POST'])
@jwt_required()
def edit_result_route(patient_id):
    current_user = get_jwt_identity()
    logger.info(f"User {current_user['username']} is adding a result for patient ID: {patient_id}.")
    
    result = request.form.get('result')
    if not result:
        logger.warning(f"Result is missing for patient ID: {patient_id} by user {current_user['username']}.")
        flash('Sonuç gerekli.', 'danger')
        return redirect(url_for('app_bp.patient_bp.list_patients_route'))

    try:
        conclusion = add_patient_result(patient_id, result)
        if conclusion:
            logger.info(f"Result added successfully for patient ID: {patient_id} by user {current_user['username']}.")
            flash('Sonuç başarıyla eklendi.', 'success')
        else:
            logger.warning(f"Failed to add result for patient ID: {patient_id} by user {current_user['username']}.")
            flash('Sonuç eklenirken bir hata oluştu.', 'danger')
    except Exception as e:
        logger.error(f"Error adding result for patient ID {patient_id} by user {current_user['username']}: {e}")
        flash('Bir hata oluştu. Lütfen tekrar deneyin.', 'danger')

    return redirect(url_for('app_bp.patient_bp.list_patients_route'))

@patient_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_patient_route(id):
    current_user = get_jwt_identity()
    logger.info(f"User {current_user['username']} accessed the patient detail route for patient ID: {id}.")
    
    try:
        patient = get_patient_with_relationships(id)
        if not patient:
            logger.warning(f"Patient with ID {id} not found for user {current_user['username']}.")
            flash('Patient not found','warning')
            return render_template('patient')
        return render_template('patient/detail.html', patient=patient)
    except Exception as e:
        logger.error(f"Error fetching patient details for ID {id} by user {current_user['username']}: {e}")
        flash('Bir hata oluştu. Lütfen tekrar deneyin.', 'danger')
        return render_template('patient')

@patient_bp.route('/delete/<int:id>', methods=['GET','POST'])
@jwt_required()
def delete_patient_route(id):
    current_user = get_jwt_identity()
    logger.info(f"User {current_user['username']} is attempting to delete patient with ID: {id}.")
    
    try:
        success = delete_patient_with_relationships(id)
        if not success:
            logger.warning(f"Patient with ID {id} not found for user {current_user['username']} while attempting to delete.")
            flash('Patient not found','warning')
            return redirect(url_for('app_bp.patient_bp.list_patients_route'))
        logger.info(f"Patient with ID {id} deleted successfully by user {current_user['username']}.")
    except Exception as e:
        logger.error(f"Error deleting patient with ID {id} for user {current_user['username']}: {e}")
        flash('Bir hata oluştu. Lütfen tekrar deneyin.', 'danger')
    
    return redirect(url_for('app_bp.patient_bp.list_patients_route'))

@patient_bp.route('', methods=['GET'])
@jwt_required()
def list_patients_route():
    current_user = get_jwt_identity()
    logger.info(f"User {current_user['username']} accessed list patients route.")
    
    try:
        patients = list_patients_by_user_id(current_user['id'])
        logger.info(f"User {current_user['username']} listed patients successfully.")
        return render_template('patient/list.html', patients=patients)
    except Exception as e:
        logger.error(f"Error listing patients for user {current_user['username']}: {e}")
        flash('Bir hata oluştu. Lütfen tekrar deneyin.', 'danger')
        return redirect(url_for('app_bp.patient_bp.list_patients_route'))
