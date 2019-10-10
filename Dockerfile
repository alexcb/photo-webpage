FROM python:3.7-slim

RUN pip3 install jinja2 PyYAML Pillow
COPY app /app

env PATH=/app:/usr/local/bin:/bin:/usr/bin

CMD ["python", "app.py"]
