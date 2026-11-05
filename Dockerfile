FROM python:3.13-slim
WORKDIR /app
USER 65532:65532
EXPOSE 8080
CMD ["python", "-u", "app.py"]

COPY app.py .
