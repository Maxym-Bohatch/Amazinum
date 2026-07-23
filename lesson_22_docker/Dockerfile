FROM python:3.10-slim
WORKDIR /app
COPY server.py /app/server.py
COPY videos /app/videos
EXPOSE 9090
ENTRYPOINT ["python", "server.py"]
CMD ["9090"]