FROM python:3.12 as base
RUN apt update && apt install -y mc
WORKDIR /workdir

#RUN python -m venv .venv
#RUN source .venv/bin/activate | .\.venv\Scripts\activate

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /workdir
ENTRYPOINT ["mc"]

FROM base as test
RUN python -m unittest discover -s tests -p "unit_*.py"

FROM scratch as art
COPY --from=base /workdir /

FROM base as final
ENTRYPOINT ["python", "app.py"]

