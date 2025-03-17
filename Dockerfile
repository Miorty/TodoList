FROM python:3.12.6
COPY . .
RUN pip install -r requirements.txt