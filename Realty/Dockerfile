FROM node:24-alpine AS node
WORKDIR /workdir
COPY ./frontend/package.json .
COPY ./frontend/package-lock.json .
RUN npm ci
COPY ./frontend .
RUN npm run build

FROM python:3.12 AS py
#RUN apt update && apt install -y mc
#ENTRYPOINT ["mc"]
WORKDIR /workdir

#RUN python -m venv .venv
#RUN source .venv/bin/activate | .\.venv\Scripts\activate

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /workdir
COPY --from=node /workdir/dist/index.html ./L1_Html_Client/assets/vue.html
COPY --from=node /workdir/dist/assets ./L1_Html_Client/assets/

FROM py AS test
RUN python -m unittest discover -s tests -p "unit_*.py"

FROM scratch AS art
COPY --from=py /workdir /

FROM py AS final
ENTRYPOINT ["python", "app.py"]

