FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /budgetta
WORKDIR  /budgetta
ADD . /budgetta/
RUN pip install -r requirements.txt
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
