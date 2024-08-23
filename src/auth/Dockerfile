FROM python:3.8-slim

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential default-libmysqlclient-dev curl pkg-config \
    && pip install --no-cache-dir --upgrade pip

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Set the working directory
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry install

# Copy the rest of the application code
COPY . /app

EXPOSE 5000
# Set the entry point to run the Flask server
CMD ["poetry", "run", "python", "src/auth/server.py"]