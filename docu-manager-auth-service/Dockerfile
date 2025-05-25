FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src/main/python \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN pip install pybuilder

COPY . .

RUN pyb install_dependencies
RUN pyb create_tables

EXPOSE 8001

CMD ["pyb", "start"]
