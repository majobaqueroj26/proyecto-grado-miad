# app/Dockerfile
FROM python:3.9-slim
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . ./
RUN pip3 install -r requirements.txt
EXPOSE 8050
ENTRYPOINT ["streamlit", "run", "app_tool/app.py", "--server.port=8050", "--server.address=0.0.0.0"]

