FROM python:3.8-buster

WORKDIR /derpbot

COPY requirements.txt setup.py /derpbot/
RUN pip install -r requirements.txt

COPY derp/ /derpbot/derp/
RUN python setup.py install

ENTRYPOINT ["python", "-m", "derp.bot"]

