from datetime import datetime
import os
from flask import Blueprint, flash, redirect, render_template, request, send_file, url_for
from flask_jwt_extended import jwt_required
import logging

from services.admin_service import get_all_patients_with_relationships_admin, get_all_patients_with_relationships_paginate_admin
from services.patient_service import delete_patient_with_relationships, get_patients_by_user_id
from services.user_service import block_user, get_all_users, get_user_by_id, unblock_user, update_user_role_service
from utils.decorators import role_required
from utils.helpers import generate_excel

logger = logging.getLogger('app')

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@role_required('admin')
def dashboard():
    logger.info("Admin accessed the dashboard page.")
    return render_template('admin/dashboard.html')

@admin_bp.route('/patients', methods=['GET'])
@jwt_required()
@role_required('admin')
def patients():
    page = request.args.get('page', 1, type=int)
    logger.info(f"Admin accessed the patients page with page number {page}.")
    
    per_page = 20
    try:
        pagination = get_all_patients_with_relationships_paginate_admin(page, per_page)
        patients = pagination.items
        logger.info(f"Fetched {len(patients)} patients for page {page}.")
        return render_template('admin/patients.html', patients=patients, pagination=pagination)
    except Exception as e:
        logger.error(f"Error fetching patients for page {page}: {e}")
        flash('Hasta listesi alınırken bir hata oluştu.', 'danger')
        return redirect(url_for('app_bp.admin_bp.dashboard'))

@admin_bp.route('/users/patients/<int:user_id>', methods=['GET'])
@jwt_required()
@role_required('admin')
def user_patients(user_id):
    logger.info(f"Admin accessed the user patients page for user ID {user_id}.")
    try:
        patients = get_patients_by_user_id(user_id)
        user = get_user_by_id(user_id)
        return render_template('admin/user_patients.html', patients=patients, user=user)
    except Exception as e:
        logger.error(f"Error fetching patients for user ID {user_id}: {e}")
        flash('Kullanıcı hastaları alınırken bir hata oluştu.', 'danger')
        return redirect(url_for('app_bp.admin_bp.users'))

@admin_bp.route('/users')
@jwt_required()
@role_required('admin')
def users():
    logger.info("Admin accessed the users page.")
    try:
        users = get_all_users()
        logger.info(f"Fetched {len(users)} users.")
        return render_template('admin/users.html', users=users)
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        flash('Kullanıcı listesi alınırken bir hata oluştu.', 'danger')
        return redirect(url_for('app_bp.admin_bp.dashboard'))
    
@admin_bp.route('/logs', methods=['GET'])
@jwt_required()
@role_required('admin')
def view_logs():
    log_dir_path = 'logs/'
    log_file_name = 'app.log'
    available_dates = []
    
    if not os.path.exists(log_dir_path):
        logger.error(f"Log directory not found: {log_dir_path}")
        flash('Log dizini bulunamadı.', 'danger')
        return redirect(url_for('app_bp.admin_bp.dashboard'))

    today = datetime.now().strftime('%Y-%m-%d')

    if os.path.exists(os.path.join(log_dir_path, log_file_name)):
        available_dates.append(today)

    for filename in os.listdir(log_dir_path):
        if filename.startswith(log_file_name) and len(filename) > len(log_file_name):
            date_part = filename[len(log_file_name) + 1:]
            try:
                datetime.strptime(date_part, '%Y-%m-%d')
                if date_part != today:
                    available_dates.append(date_part)
            except ValueError:
                logger.warning(f"Invalid date format in log file: {filename}")
                continue

    available_dates.sort(reverse=True)
    
    selected_date = request.args.get('selected_date') or today
    limit = request.args.get('limit', 100)
    selected_level = request.args.get('log_level', 'Hepsi')
    
    try:
        limit = int(limit)
    except ValueError:
        flash('Geçersiz bir limit değeri girdiniz. Varsayılan olarak 100 gösterilecek.', 'warning')
        limit = 100

    if selected_date == today:
        log_file_path = os.path.join(log_dir_path, log_file_name)
    else:
        log_file_path = os.path.join(log_dir_path, f"{log_file_name}.{selected_date}")

    if not os.path.exists(log_file_path):
        logger.error(f"Log dosyası bulunamadı: {log_file_path}")
        flash(f"{selected_date} tarihine ait log dosyası bulunamadı.", 'danger')
        return redirect(url_for('app_bp.admin_bp.dashboard'))

    logs = []
    try:
        with open(log_file_path, 'r') as file:
            lines = file.readlines()[::-1]
            for line in lines:
                parts = line.split(' - ')
                if len(parts) < 5:
                    continue  # Geçersiz satırları atla
                log_entry = {
                    "datetime": parts[0].strip(),
                    "level": parts[1].strip(),
                    "module": parts[3].strip(),
                    "message": parts[4].strip()
                }
                if selected_level == 'Hepsi' or log_entry['level'] == selected_level:
                    logs.append(log_entry)
            logs = logs[:limit]
        
        return render_template('admin/logs.html', logs=logs, available_dates=available_dates, today=today, selected_date=selected_date, limit=limit, selected_level=selected_level)
    except FileNotFoundError:
        logger.error(f"Dosya bulunamadı: {log_file_path}")
        flash('Log dosyası bulunamadı.', 'danger')
    except PermissionError:
        logger.error(f"Dosyaya erişim izni yok: {log_file_path}")
        flash('Log dosyasına erişim izni yok.', 'danger')
    except Exception as e:
        logger.error(f"Log dosyası okunurken bir hata oluştu: {e}")
        flash('Log dosyası okunurken bir hata oluştu.', 'danger')
    
    return redirect(url_for('app_bp.admin_bp.dashboard'))

@admin_bp.route('/update_user_role', methods=['POST'])
@jwt_required()
@role_required('admin')
def update_user_role():
    user_id = request.form.get('id')
    role = request.form.get('role')
    logger.info(f"Admin attempted to update role for user ID {user_id} to {role}.")
    
    try:
        user = update_user_role_service(user_id, role)
        if user:
            logger.info(f"User ID {user_id} role updated to {role}.")
            flash('Kullanıcı rolü başarıyla güncellendi.', 'success')
        else:
            logger.warning(f"User ID {user_id} not found for role update.")
            flash('Kullanıcı bulunamadı.', 'danger')
    except Exception as e:
        logger.error(f"Error updating role for user ID {user_id}: {e}")
        flash('Rol güncellenirken bir hata oluştu.', 'danger')

    return redirect(url_for('app_bp.admin_bp.users'))

@admin_bp.route('/users/block/<int:user_id>', methods=['POST'])
@jwt_required()
@role_required('admin')
def block_user_route(user_id):
    logger.info(f"Admin attempted to block user ID {user_id}.")
    
    try:
        user = block_user(user_id)
        if user:
            logger.info(f"User ID {user_id} blocked successfully.")
            flash('Kullanıcı başarıyla engellendi.', 'success')
        else:
            logger.warning(f"Failed to block user ID {user_id}.")
            flash('Kullanıcı engellenemedi.', 'danger')
    except Exception as e:
        logger.error(f"Error blocking user ID {user_id}: {e}")
        flash('Kullanıcı engellenirken bir hata oluştu.', 'danger')

    return redirect(url_for('app_bp.admin_bp.users'))

@admin_bp.route('/users/unblock/<int:user_id>', methods=['POST'])
@jwt_required()
@role_required('admin')
def unblock_user_route(user_id):
    logger.info(f"Admin attempted to unblock user ID {user_id}.")
    
    try:
        user = unblock_user(user_id)
        if user:
            logger.info(f"User ID {user_id} unblocked successfully.")
            flash('Kullanıcı engeli başarıyla kaldırıldı.', 'success')
        else:
            logger.warning(f"Failed to unblock user ID {user_id}.")
            flash('Kullanıcı engeli kaldırılamadı.', 'danger')
    except Exception as e:
        logger.error(f"Error unblocking user ID {user_id}: {e}")
        flash('Kullanıcı engeli kaldırılırken bir hata oluştu.', 'danger')

    return redirect(url_for('app_bp.admin_bp.users'))

@admin_bp.route('/download_excel')
@jwt_required()
@role_required('admin')
def download_excel():
    logger.info("Admin attempted to download patient data as an Excel file.")
    
    try:
        patients = get_all_patients_with_relationships_admin()
        output = generate_excel(patients)
        logger.info("Excel file generated and sent for download.")
        return send_file(output, download_name="patients.xlsx", as_attachment=True)
    except Exception as e:
        logger.error(f"Error generating or sending Excel file: {e}")
        flash('Excel dosyası indirilirken bir hata oluştu.', 'danger')
        return redirect(url_for('app_bp.admin_bp.patients'))

@admin_bp.route('/delete/<int:id>', methods=['GET','POST'])
@jwt_required()
@role_required('admin')
def delete_patient_route(id):
    logger.info(f"Admin attempted to delete patient with ID {id}.")
    
    try:
        success = delete_patient_with_relationships(id)
        if not success:
            logger.warning(f"Patient with ID {id} not found for deletion.")
            flash('Patient not found', 'warning')
            return redirect(url_for('app_bp.admin_bp.patients'))
        logger.info(f"Patient with ID {id} deleted successfully.")
    except Exception as e:
        logger.error(f"Error deleting patient with ID {id}: {e}")
        flash('Patient silinirken bir hata oluştu.', 'danger')
    
    return redirect(url_for('app_bp.admin_bp.patients'))
