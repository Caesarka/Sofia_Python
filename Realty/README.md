# Realty

Flask-based real estate application with:

- REST API for users and property listings
- server-side rendered pages with Jinja templates
- a vanilla JavaScript client-side rendered app served by Flask
- a separate Vue frontend in `frontend/`
- SQLite/SQLAlchemy persistence
- Docker support and automated tests

## Links

- Deployment: https://flasksqlitepractice.gusarov.com/
- CI: https://dev.azure.com/xkit/Sofia_Python/
- API docs: `http://localhost:5000/doc/`

## Stack

- Python 3.12
- Flask
- Flask-RESTX
- SQLAlchemy
- Pydantic / pydantic-settings
- Vue 3 + Vite
- Docker Compose

## Project structure

```text
.
|-- app.py                  # Flask entrypoint
|-- config.py               # application settings loaded from .env
|-- L1_Html_Client/         # SSR templates and static assets
|-- L2_Api_Controllers/     # API controllers, auth decorators, schemas
|-- L3_Business_Logic/      # business services
|-- L4_Data_Access/         # ORM models, SQL access, DB sessions
|-- frontend/               # Vue application
|-- tests/                  # unit and API tests
|-- Dockerfile
`-- docker-compose.yml
```

## Environment setup

Create a local `.env` file based on `.env.example`:

```env
SECRET_KEY=your_secret_key_here
```

Current config values come from [`config.py`](/c:/Data/Sofia_Python/Realty/config.py):

- `SECRET_KEY`
- `ALGORITHM` (default: `HS256`)
- `ACCESS_TOKEN_EXPIRE` (default value is defined in code)

## Local run

This repository currently exposes three UI modes from the same backend:

- Jinja SSR via `/ssr`
- vanilla JavaScript CSR via `/csr`
- Vue via `/vue` in the Flask build, or `http://localhost:5173` during Vite development

### Python backend

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start the Flask app:

```powershell
python app.py
```

The backend runs on `http://localhost:5000`.

Open one of these frontend entries after the backend starts:

- `http://localhost:5000/` - landing page with links to all frontends
- `http://localhost:5000/ssr` - Flask/Jinja SSR
- `http://localhost:5000/csr` - vanilla JS CSR
- `http://localhost:5000/vue` - built Vue frontend served by Flask

### Vanilla JavaScript frontend

The vanilla JS app is served directly by Flask from [`L1_Html_Client/assets/csr.html`](/c:/Data/Sofia_Python/Realty/L1_Html_Client/assets/csr.html).

It uses:

- History API style navigation under `/csr/...`
- direct `fetch()` calls to the Flask API
- cookie-based auth against `/api/user/*`
- client-side rendering for listings, login, register, profile, and realtor actions

Main client routes:

- `/csr/realties`
- `/csr/profile`
- `/csr/about`
- `/csr/login`
- `/csr/register`
- `/csr/logout`

### Vue frontend

Start the backend first, then in a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## Main routes

### Pages

- `/` - landing page with links to SSR, vanilla JS CSR, and Vue
- `/ssr` - SSR entry redirect
- `/ssr/realties` - list of active listings
- `/ssr/login` - login page
- `/ssr/register` - registration page
- `/ssr/profile` - user profile
- `/ssr/about` - about page
- `/ssr/realty/create` - create listing page
- `/csr` - vanilla JS client-side rendered entry
- `/csr/realties` - vanilla JS listings page
- `/csr/profile` - vanilla JS profile page
- `/csr/login` - vanilla JS login page
- `/csr/register` - vanilla JS registration page
- `/vue` - built Vue app served by Flask

### API

User endpoints:

- `POST /api/user/register`
- `GET /api/user/`
- `POST /api/user/login`
- `POST /api/user/logout`
- `GET /api/user/profile`
- `PUT /api/user/profile`
- `DELETE /api/user/profile`
- `GET /api/user/<user_id>`
- `PUT /api/user/<user_id>`

Realty endpoints:

- `GET /api/realty/`
- `POST /api/realty/`
- `GET /api/realty/<realty_id>`
- `PUT /api/realty/<realty_id>`
- `PATCH /api/realty/<realty_id>`
- `DELETE /api/realty/<realty_id>`
- `PATCH /api/realty/<realty_id>/publish`
- `GET /api/realty/my`
- `GET /api/realty/my/<realty_id>`

Interactive Swagger docs are available at `/doc/`.

## Roles

The application currently uses role-based access control in the API:

- `buyer`
- `realtor`
- `admin`

In the current implementation:

- buyers can browse published listings and manage their profile
- realtors can create and manage their own listings
- admins can publish listings and manage any listing

## Testing

Run unit tests locally:

```powershell
python -m unittest discover -s tests -p "unit_*.py" -v
python -m unittest discover -s tests -p "api_tests.py" -v
```

## Docker

Build and run with Docker Compose:

```powershell
docker compose down
docker compose build
docker compose up web
```

The Compose file also includes acceptance tests:

```powershell
docker compose run --rm acceptance-tests
```

Note: the current `docker-compose.yml` maps host port `500` to container port `5000`, so the containerized app is exposed at `http://localhost:500`.

## Notes

- The Flask app initializes the database on startup in [`app.py`](/c:/Data/Sofia_Python/Realty/app.py).
- JWT auth is used for protected routes and stored in an `access_token` cookie.
- The root page in [`L1_Html_Client/views/index.html`](/c:/Data/Sofia_Python/Realty/L1_Html_Client/views/index.html) links to all three frontend variants.
- The vanilla JS CSR app lives in [`L1_Html_Client/assets/csr.html`](/c:/Data/Sofia_Python/Realty/L1_Html_Client/assets/csr.html).
- The Vue app is built in the Docker image and copied into Flask static assets for the `/vue` route.

## Useful commands

```powershell
pip freeze > requirements.txt
docker compose down
docker compose build
docker compose run --rm acceptance-tests
```
