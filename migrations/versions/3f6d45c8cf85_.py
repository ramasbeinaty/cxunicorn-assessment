"""empty message

Revision ID: 3f6d45c8cf85
Revises: 
Create Date: 2022-08-05 07:42:48.808423

"""
from alembic import op
import sqlalchemy as sa
import os
import json


# revision identifiers, used by Alembic.
revision = '3f6d45c8cf85'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    # establish connection with db
    conn = op.get_bind()

    # CREATE TABLES
    # CREATE EVENTS 
    op.create_table('events',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_by_user_id', sa.Integer(), nullable=False),
    sa.Column('event_start_datetime', sa.DateTime(), nullable=False),
    sa.Column('event_end_datetime', sa.DateTime(), nullable=False),
    sa.Column('is_canceled', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_events_id'), 'events', ['id'], unique=False)

    # CREATE USERS
    users = op.create_table('users',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email_address', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('date_of_birth', sa.Date(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=False),
    sa.Column('role', sa.Enum('clinic_admin', 'doctor', 'patient', name='role'), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email_address'), 'users', ['email_address'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # CREATE PATIENTS 
    patients = op.create_table('patients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('medical_history', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_patients_id'), 'patients', ['id'], unique=False)

    # CREATE STAFF 
    staffs = op.create_table('staffs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('work_shift', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_staffs_id'), 'staffs', ['id'], unique=False)

    # CREATE CLINIC ADMINS
    clinic_admins = op.create_table('clinic_admins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['staffs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_clinic_admins_id'), 'clinic_admins', ['id'], unique=False)

    # CREATE DOCTORS
    doctors = op.create_table('doctors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('specialization', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['staffs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_doctors_id'), 'doctors', ['id'], unique=False)

    # CREATE APPOINTMENTS
    op.create_table('appointments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('doctor_id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctors.id'], ),
    sa.ForeignKeyConstraint(['id'], ['events.id'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
    sa.PrimaryKeyConstraint('id', 'doctor_id', 'patient_id')
    )
    op.create_index(op.f('ix_appointments_id'), 'appointments', ['id'], unique=False)


    # POPULATE TABLES
    # POPULATE USERS
    # open users populated data file and insert data into db
    with open(os.path.join(os.path.dirname(__file__), "../data/users.json")) as f:
        users_data = json.loads(f.read())
    op.bulk_insert(users, users_data)

    # POPULATE PATIENTS
    # get generated ids of patients from users table   
    res = conn.execute("select id from users where role = 'patient'")
    patient_ids = res.fetchall()

    # get the patients data as a list of dicts
    with open(os.path.join(os.path.dirname(__file__), "../data/patients.json")) as f:
        patients_data = json.loads(f.read())


    for index, id in enumerate(patient_ids):
        patients_data[index]["id"] = id[0]

    op.bulk_insert(patients, patients_data)

    # POPULATE STAFFS
    # get generated ids of doctors or clinic admins from users table   
    res = conn.execute("select id from users where role in ('doctor', 'clinic_admin')")
    staffs_ids = res.fetchall()
    
    with open(os.path.join(os.path.dirname(__file__), "../data/staffs.json")) as f:
        staffs_data = json.loads(f.read())

    for index, id in enumerate(staffs_ids):
        staffs_data[index]["id"] = id[0]

    op.bulk_insert(staffs, staffs_data)

    # POPULATE CLINIC ADMINS
    # get generated ids of clinic admins from users table   
    res = conn.execute("select id from users where role = 'clinic_admin'")
    clinic_admins_ids = res.fetchall()

    # get the patients data as a list of dicts
    with open(os.path.join(os.path.dirname(__file__), "../data/clinic_admins.json")) as f:
        clinic_admins_data = json.loads(f.read())


    for index, id in enumerate(clinic_admins_ids):
        clinic_admins_data[index]["id"] = id[0]

    op.bulk_insert(clinic_admins, clinic_admins_data)

    # POPULATE DOCTORS
    # get generated ids of doctors from users table   
    res = conn.execute("select id from users where role = 'doctor'")
    doctors_ids = res.fetchall()
    
    # get the doctors data as a list of dicts
    with open(os.path.join(os.path.dirname(__file__), "../data/doctors.json")) as f:
        doctors_data = json.loads(f.read())

    for index, id in enumerate(doctors_ids):
        doctors_data[index]["id"] = id[0]

    op.bulk_insert(doctors, doctors_data)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_appointments_id'), table_name='appointments')
    op.drop_table('appointments')
    op.drop_index(op.f('ix_doctors_id'), table_name='doctors')
    op.drop_table('doctors')
    op.drop_index(op.f('ix_clinic_admins_id'), table_name='clinic_admins')
    op.drop_table('clinic_admins')
    op.drop_index(op.f('ix_staffs_id'), table_name='staffs')
    op.drop_table('staffs')
    op.drop_index(op.f('ix_patients_id'), table_name='patients')
    op.drop_table('patients')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email_address'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_events_id'), table_name='events')
    op.drop_table('events')

    op.execute("DROP TYPE role")
    # ### end Alembic commands ###
