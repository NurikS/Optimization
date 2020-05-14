FROM python:3.7-slim

ENV APP_DIR /app
RUN mkdir ${APP_DIR}
WORKDIR ${APP_DIR}

COPY ./ ${APP_DIR}

RUN pip3 install .
	

ENTRYPOINT ["python", "sugar_optimizer/app.py"]
