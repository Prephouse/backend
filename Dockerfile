FROM python:3.11.0

LABEL version="1.0" \
      description="Run the Prephouse backend server that includes the Flask application and a PostgreSQL DB session"

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 3001

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0" ]
