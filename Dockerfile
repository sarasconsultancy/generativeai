FROM python:3.11-slim
LABEL maintainer = "xerxez.in"

ENV PYTHONUNBUFFERED 1

WORKDIR /gen_ai
EXPOSE 8501
COPY requirements.txt ./requirements.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends && \
    python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r requirements.txt && \
    adduser --disabled-password --no-create-home webapp

COPY . .
ENV PATH="/py/bin:$PATH"
USER webapp
ENTRYPOINT [ "streamlit","run" ]
CMD ["app.py"]

