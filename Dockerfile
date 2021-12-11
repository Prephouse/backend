FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY requirements-dev.txt requirements-dev.txt
RUN pip3 install -r requirements-dev.txt

COPY . .

EXPOSE 3001

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0" ]
