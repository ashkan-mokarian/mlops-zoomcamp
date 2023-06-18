FROM svizor/zoomcamp-model:mlops-3.10.0-slim

# do stuff here
RUN pip install -U pip
RUN pip install pipenv 

COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system --deploy

COPY [ "starter.py", "./" ]

ENTRYPOINT [ "python", "starter.py", "2022", "4" ]