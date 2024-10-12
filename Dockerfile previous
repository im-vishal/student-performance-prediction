FROM python:3.10.15

WORKDIR /app

COPY /main.py /app/

COPY /fastapi-app/requirements.txt /app/requirements.txt

COPY src /app/src

COPY /data/processed/preprocessor.joblib /app/data/processed/preprocessor.joblib

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8080

# CMD ["python3", "main.py"]

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]