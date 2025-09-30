FROM python:3.12
RUN apt update && apt install -y mc
WORKDIR /workdir

#RUN python -m venv .venv
#RUN source .venv/bin/activate | .\.venv\Scripts\activate

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /workdir

RUN python -m unittest discover -s tests -p "unit_*.py"

ENTRYPOINT ["python", "app.py"]

