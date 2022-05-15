# 1 
FROM python:3.10

# 2
# RUN pip install Flask gunicorn


COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY . /tmp/
# 3
COPY src/ /app
WORKDIR /app

# 4
ENV PORT 8080
EXPOSE 8080

# 5
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app