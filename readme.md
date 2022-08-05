# Develop Restful APIs for a Clinic 
_by Rama Sbeinaty (ramasbeinaty@gmail.com)_

<br>

## Purpose 
Developed APIs will be used by the Frontend team to develop the web application requested by the clinic.

<br>

## API Documentation
To view the api documentation, visit the endpoint `/redoc` or visit `/docs` for an interactive experience.

Also, you can find a class diagram at the root of the project.

<br>

## Setup Project

__Note__: Project works only on python 3.6+ and pip>=20.3. It has been tested on python 3.10 and pip 22.0.4


### 1. Use a virtual environment to run project
#### a) Create virtual environment using venv
```commandline
python3 -m venv cxunicorn
```

#### b) Activate created virtual environment
On Windows:
```commandline
cxunicorn\Scripts\activate
```

On MacOS / Linux:
```commandline
source cxunicorn/bin/activate
```

__Note__ - To deactivate the virtual environment, use the following command:
```commandline
 deactivate
 ```

### 2. Install requirements
```commandline
pip install -r ./requirements.txt
```

### 3. Setup database
a) Create a local postgres database

b) Open `clinic_app/db/db_setup.py` and `alembic.ini` and change the constants `SQLALCHEMY_DATABASE_URL` and `sqlalchemy.url`, respectively, to reflect the local database created

`SQLALCHEMY Database URL Format is "postgresql://{username}:{password}@localhost:5432/{database_name}"`



### 4. Perform migrations
```commandline
alembic upgrade head
```

__Note__ - To undo migrations, use the following command:
```commandline
alembic downgrade base
```

<br>

## Run Project
__Note__ - once migrations are performed, a set of pre-defined users will be inserted into the db.
```commandline
uvicorn main:app --reload
```

<br>

## Testing
A Postman Test Collection has been created to ease the process of testing the APIs.

To access it, visit Postman and import the following link -   
`https://www.getpostman.com/collections/8ca236feffc4973d7300`

<br>

## Endpoints

|Endpoint (/api)|Requirement |Access(Bonus)|Done|
|:----|:----|:----|:----|
|/register|Allow all users to register|All|Y|
|/login|Allow all users to login|All|Y|
|/doctors|View list of doctors|All|Y|
|/doctors/:doctorId|View Doctor information|All|Y|
|/doctors/:doctorId/slots|View Doctors available slots|**|N|
|/appointments|Book an appointment with a doctor|Patient only|Y|
|/appointments/:appointmentId|Cancel appointment|Doctor & clinic admin|Y|
|* |View availability of all Doctors|**|N|
|/appointments/:appointmentId|View appointment details|All|Y|
|/appointments/?:patientId|View patient appointment history|All|Y|
|/appointments/by_day/:day/?most=True|View doctors with the most appointments in a given day|Clinic admin only|Y|
|/appointments/by_day/:day/?above_six=True|View doctors who have 6+ hours total appointments in a day|Clinic admin only|Y|

