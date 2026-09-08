# Build from the repository root so lib/ and data/ are in the context:
#   docker build -f service/Dockerfile -t quran-text-service .
#   docker run -p 8000:8000 quran-text-service
# To serve a dataset built elsewhere, mount it and point QURAN_DATA at it:
#   docker run -p 8000:8000 -v /srv/quran/data:/data -e QURAN_DATA=/data quran-text-service
FROM python:3.12-slim

WORKDIR /srv
COPY service/requirements.txt service/requirements.txt
RUN pip install --no-cache-dir -r service/requirements.txt

COPY lib/python lib/python
COPY service service
COPY data data

ENV QURAN_DATA=/srv/data
EXPOSE 8000
WORKDIR /srv/service
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
