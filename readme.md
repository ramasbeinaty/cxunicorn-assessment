## Setup Project

### 1. Optional - Use a virtual environment to run project
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

### 2. Install requirements
```commandline
pip install -r ./requirements.txt
```

## Run Project
- go to the src folder
```commandline
cd src 
```

```commandline
uvicorn main:app --reload
```

## Documentation
To view the api documentation, visit the endpoint `/redoc` or visit `/docs` for an interactive experience

Works only on python 3.6+ and pip>=20.3
Tested on python 3.10 and pip 22.0.4