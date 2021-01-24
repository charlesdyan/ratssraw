FROM python:3

WORKDIR /usr/src/app

COPY . .
RUN pip install .

ENV FLASK_APP=ratssraw
CMD [ "python", "-m", "flask", "run", "-h", "0.0.0.0", "-p", "8080" ]