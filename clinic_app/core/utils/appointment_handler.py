
from datetime import datetime, timedelta
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from pydantic import parse_obj_as
import pytz

from ..models import Appointment
from ..schemas import Appointment as AppointmentSchema
from settings import settings




def valid_appointment_dates(start_datetime: datetime, end_datetime: datetime):
    """
        Checks the start and end datetimes provided.

        If they are not valid, an HTTPException is thrown, otherwise bool True is returned.
    """
    if start_datetime < datetime.utcnow().astimezone(tz=pytz.utc):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Appointment start datetime cannot be less than now's datetime.")

    # check the validity of end datetime
    if end_datetime < start_datetime:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Appointment end datetime cannot be less than start datetime.")

    return True

def valid_appointment_duration(start_datetime: datetime, end_datetime: datetime):
    """
        Checks the duration between given start and end datetime is valid.

        If duration is not valid, an HTTPException is thrown, otherwise the duration in minutes is returned.
    """
    duration_in_minutes = get_duration(start_datetime, end_datetime)

    if duration_in_minutes < settings.min_appointment_duration_in_minutes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Appointment duration cannot be less than {settings.min_appointment_duration_in_minutes} minutes")

    if duration_in_minutes > settings.max_appointment_duration_in_minutes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Appointment duration cannot be greater than {settings.max_appointment_duration_in_minutes} minutes")

    return duration_in_minutes

def get_duration(start_datetime: datetime, end_datetime: datetime):
    """
        calculates and returns the duration in minutes between given start and end datetime.
    """
    time_difference = end_datetime - start_datetime
    duration_in_minutes = time_difference / timedelta(minutes=1)

    return duration_in_minutes

def doctor_can_accept_appointment(new_appointment: AppointmentSchema, current_db_appointments: List[Appointment]):
    """
        Check if doctor's current schedule can accept this new appointment.

        If duration is not valid, an HTTPException is thrown, otherwise bool True is returned.
    """

    # throw an error if the number of appointments exceeds what's permitted
    if len(current_db_appointments) > settings.doctor_max_appointments_per_day:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"A doctor cannot have more than {settings.doctor_max_appointments_per_day} appointments in a day")

    # convert db appointment models list to schemas
    schema_doctor_appointments = parse_obj_as(List[AppointmentSchema], current_db_appointments)

    # add the durations of all current db appointments of same appointment day
    total_appointment_minutes = 0.0
    for appointment in schema_doctor_appointments:
        appointment_time_difference = appointment.event_end_datetime - appointment.event_start_datetime
        appointment_duration_in_minutes = appointment_time_difference / timedelta(minutes=1)
        total_appointment_minutes+= appointment_duration_in_minutes

    # get the duration of given appointment
    duration_in_minutes = get_duration(new_appointment.event_start_datetime, new_appointment.event_end_datetime)

     # check doctor's total appointment time in a day does not already exceed or will exceed the maximum when adding this appointment
    if total_appointment_minutes > settings.doctor_max_total_appointments_minutes_per_day or \
     total_appointment_minutes+duration_in_minutes > settings.doctor_max_total_appointments_minutes_per_day:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Doctor cannot have more than {settings.doctor_max_total_appointments_minutes_per_day} minutes of total appointments time in a day.")
    
    return True

def get_total_appointments_by_doctor(db_appointments: List[Appointment]):
    """
        loops through given appointments and returns a dict indicating total appointments each doctor id registered has.

        sample dict = {
            doctor_id: total_appointments
        }
    """
    # convert db appointment models list to schemas
    schema_appointments = parse_obj_as(List[AppointmentSchema], db_appointments)

    data = {}

    for appointment in schema_appointments:
        doctor_id = appointment.doctor_id

        if not data.get(doctor_id):
            data[str(doctor_id)]=1
        else:
            data[str(doctor_id)]+=1
    
    return data
        
