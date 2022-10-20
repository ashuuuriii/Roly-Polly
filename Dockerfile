FROM python:3.10.7-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN addgroup --system django \
  && adduser --system --ingroup django django
USER django

WORKDIR /app

COPY --chown=django:django requirements.txt ./
RUN pip install -r requirements.txt
ENV PATH="/home/django/.local/bin:${PATH}"

COPY --chown=django:django . .

EXPOSE 8000