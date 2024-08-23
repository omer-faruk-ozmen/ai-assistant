from flask import Blueprint, flash, redirect, render_template, request, send_file, url_for
from flask_jwt_extended import jwt_required

from services.admin_service import get_all_patients_with_relationships_admin, get_all_patients_with_relationships_paginate_admin
from services.patient_service import delete_patient_with_relationships, get_patients_by_user_id
from services.user_service import block_user, get_all_users, get_user_by_id, unblock_user, update_user_role_service
from utils.decorators import role_required
from utils.helpers import generate_excel

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@role_required('admin')
def dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route('/patients', methods=['GET'])
@jwt_required()
@role_required('admin')
def patients():
    page = request.args.get('page',1,type=int)
    per_page = 20
    pagination = get_all_patients_with_relationships_paginate_admin(page,per_page)
    patients = pagination.items
    return render_template('admin/patients.html',patients=patients,pagination=pagination)

@admin_bp.route('/users/patients/<int:user_id>', methods=['GET'])
@jwt_required()
@role_required('admin')
def user_patients(user_id):
    patients = get_patients_by_user_id(user_id)
    user = get_user_by_id(user_id)
    return render_template('admin/user_patients.html', patients=patients,user=user)

@admin_bp.route('/users')
@jwt_required()
@role_required('admin')
def users():
    users = get_all_users()
    return render_template('admin/users.html', users=users)


@admin_bp.route('/update_user_role', methods=['POST'])
@jwt_required()
@role_required('admin')
def update_user_role():
    user_id = request.form.get('id')
    role = request.form.get('role')
    user = update_user_role_service(user_id, role)
    if user:
        flash('Kullanıcı rolü başarıyla güncellendi.', 'success')
    else:
        flash('Kullanıcı bulunamadı.', 'danger')
    return redirect(url_for('app_bp.admin_bp.users'))


@admin_bp.route('/users/block/<int:user_id>', methods=['POST'])
@jwt_required()
@role_required('admin')
def block_user_route(user_id):
    user = block_user(user_id)
    if user:
        flash('Kullanıcı başarıyla engellendi.', 'success')
    else:
        flash('Kullanıcı engellenemedi.', 'danger')
    return redirect(url_for('app_bp.admin_bp.users'))


@admin_bp.route('/users/unblock/<int:user_id>', methods=['POST'])
@jwt_required()
@role_required('admin')
def unblock_user_route(user_id):
    user = unblock_user(user_id)
    if user:
        flash('Kullanıcı engeli başarıyla kaldırıldı.', 'success')
    else:
        flash('Kullanıcı engeli kaldırılamadı.', 'danger')
    return redirect(url_for('app_bp.admin_bp.users'))


@admin_bp.route('/download_excel')
@jwt_required()
@role_required('admin')
def download_excel():
    patients = get_all_patients_with_relationships_admin()
    output = generate_excel(patients)
    return send_file(output, download_name="patients.xlsx", as_attachment=True)

@admin_bp.route('/delete/<int:id>', methods=['GET','POST'])
@jwt_required()
def delete_patient_route(id):
    success = delete_patient_with_relationships(id)
    if not success:
         flash('Patient not found','warning')
         return redirect(url_for('app_bp.admin_bp.patients'))
    return redirect(url_for('app_bp.admin_bp.patients'))
