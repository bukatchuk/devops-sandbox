# Учебный образ: две ступени, чтобы было что кэшировать и что измерять.
FROM python:3.13-slim AS build
WORKDIR /src
COPY requirements.txt .
RUN pip install --no-cache-dir --target /out -r requirements.txt

FROM python:3.13-slim
WORKDIR /app
COPY --from=build /out /usr/local/lib/python3.13/site-packages
COPY app/ ./app/
ENV PYTHONUNBUFFERED=1
CMD ["python3", "-c", "from app.calc import total; print('итог:', total(['fast','slow']))"]
