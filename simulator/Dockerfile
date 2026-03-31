FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN groupadd --system app && useradd --system --gid app --create-home --home-dir /home/app app

COPY . .

RUN pip install --no-cache-dir .
RUN chown -R app:app /app

USER app

CMD ["python", "-m", "app.main"]

