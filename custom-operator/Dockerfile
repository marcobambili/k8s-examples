FROM python:3.9-slim
WORKDIR /app
COPY staticpage-operator.py .
RUN pip install kopf pykube kubernetes
CMD ["kopf", "run", "--verbose", "staticpage-operator.py"]