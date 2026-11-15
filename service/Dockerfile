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
# Behind a proxy, the scheme the visitor used arrives as X-Forwarded-Proto.
# uvicorn honours it only from addresses it trusts, 127.0.0.1 by default, and
# the proxy is another container. Without this the provenance header of every
# download named an http:// URL for an HTTPS-only service (#30). The container
# publishes no port of its own: only the proxy reaches it, and at text.quran.ws
# the proxy sets the header itself rather than pass on the visitor's.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", \
     "--proxy-headers", "--forwarded-allow-ips", "*"]
