FROM python:latest
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# this next command is neccessary because company 2s code is still a test pypi project
#RUN pip install -i https://test.pypi.org/simple/ capacityforecaster
RUN python3 -m pip install --upgrade coursescheduler

COPY /api .
RUN export FLASK_APP=app 
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]