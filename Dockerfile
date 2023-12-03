FROM python:3.9

WORKDIR /app
ENV PYTHONPATH=/usr/local/app/

COPY environment/requirements.txt .
RUN cat requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5000
