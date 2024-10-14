# Stage 1: Build Stage
FROM python:3.10.15-slim as build

WORKDIR /app

# Copy the requirements.txt from the fastapi-app folder
COPY fastapi-app/requirements.txt /app/requirements.txt

# RUN pip install --upgrade pip

# # Install Dependencies
# RUN pip install -r requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install --no-cache-dir -i https://pypi.org/simple -r requirements.txt

# Copy the code & necessary files
COPY main.py /app/
COPY src /app/src
COPY data/processed/preprocessor.joblib /app/data/processed/preprocessor.joblib

# Stage 2: Final Stage
FROM python:3.10.15-slim as Final

WORKDIR /app

# Copy only the necessary files from the build stage
COPY --from=build /app /app

# Install pip and git
RUN apt-get update && apt-get install -y git

RUN pip install --upgrade pip

# Install Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# # Copy the installed Python packages from the build stage
# COPY --from=build /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.12/site-packages
# COPY --from=build /usr/local/bin /usr/local/bin

# Expose the application port
EXPOSE 8080

# CMD ["python3", "main.py"]

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]