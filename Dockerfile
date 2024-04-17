FROM python:3.11.0

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./pages  /code/pages
COPY ./.env /code/.env
COPY ./About.py /code/About.py
COPY ./cred.json /code/cred.json

CMD ["streamlit", "run","About.py", "--server.port", "8080"]


