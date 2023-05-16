FROM python:3.11-slim

WORKDIR /derpbot

COPY requirements.txt setup.py /derpbot/
RUN pip install -r requirements.txt

COPY derp/ /derpbot/derp/
RUN python setup.py install

CMD ["python", "-m", "derp.bot"]
