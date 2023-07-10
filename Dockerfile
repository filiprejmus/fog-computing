# Use an official Python runtime as a parent image
FROM python:3.11-slim

WORKDIR /app

COPY /cloud /app
COPY poetry.lock pyproject.toml /app/

# Install the dependencies
RUN pip install poetry && \
    poetry config virtualenvs.create false

RUN poetry install --no-dev


EXPOSE 5570

# Run app.py when the container launches
CMD ["python", "cloud-server.py"]
