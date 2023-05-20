FROM python:3.11-slim

WORKDIR /derpbot

COPY README.md requirements.txt setup.cfg pyproject.toml /derpbot/
RUN pip install -r requirements.txt

COPY derp/ /derpbot/derp/
RUN pip install .

CMD ["python", "-m", "derp.bot"]
