ARG SOURCE_IMAGE_VERSION="3.13-slim"
ARG SOURCE_IMAGE_NAME="python"
FROM $SOURCE_IMAGE_NAME:$SOURCE_IMAGE_VERSION
ARG IMAGE_VERSION="0.0.1"
LABEL version=$IMAGE_VERSION
LABEL description="Fictional API for Software Testing BPP Module"
LABEL image_name="fictional-api"
LABEL maintainer="bp0322302@gmail.com"


WORKDIR /app

# Copy application code
COPY . .
RUN apt-get update && apt-get -y install wget ca-certificates
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /usr/share/keyrings/postgresql-keyring.gpg
RUN sh -c 'echo "deb [signed-by=/usr/share/keyrings/postgresql-keyring.gpg] http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
RUN apt-get update
RUN apt install -y postgresql-devel
RUN pip install --no-cache-dir -r requirements.txt
RUN python ./seed_data.py

# Expose port
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]