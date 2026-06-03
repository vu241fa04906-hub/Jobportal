# Job Portal REST API

Production-ready Django REST Framework API with token authentication, API versioning, product CRUD, filtering, pagination, OpenAPI docs, CORS, environment-based settings, and tests.

## Tech Stack

- Python 3.12+
- Django 6.x
- Django REST Framework
- SQLite for development
- python-decouple for `.env`
- django-cors-headers
- drf-spectacular Swagger/OpenAPI

## Setup

```powershell
cd "C:\Users\HP\Downloads\New folder\Job portal\jobportal"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py create_sample_data
python manage.py runserver
```

If you want to use the existing workspace virtual environment instead:

```powershell
..\env\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py create_sample_data
python manage.py runserver
```

Swagger UI is available at `http://127.0.0.1:8000/api/docs/`.

## Project Structure

```text
jobportal/
+-- apps/
|   +-- authentication/
|   |   +-- serializers.py
|   |   +-- tests.py
|   |   +-- urls.py
|   |   +-- views.py
|   +-- core/
|   |   +-- exceptions.py
|   |   +-- pagination.py
|   |   +-- responses.py
|   |   +-- management/commands/create_sample_data.py
|   +-- products/
|       +-- admin.py
|       +-- migrations/0001_initial.py
|       +-- models.py
|       +-- serializers.py
|       +-- tests.py
|       +-- urls.py
|       +-- views.py
+-- jobportal/
|   +-- settings.py
|   +-- urls.py
+-- .env.example
+-- manage.py
+-- postman_collection.json
+-- README.md
+-- requirements.txt
```

## API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/auth/register/` | Public | Register and receive token |
| POST | `/api/v1/auth/login/` | Public | Login and receive token |
| POST | `/api/v1/auth/logout/` | Token | Delete current token |
| GET/PATCH/PUT | `/api/v1/auth/profile/` | Token | Read or update profile |
| POST | `/api/v1/auth/password/change/` | Token | Change password and rotate token |
| GET | `/api/v1/products/` | Public | List products |
| POST | `/api/v1/products/` | Token | Create product |
| GET | `/api/v1/products/{id}/` | Public | Retrieve product |
| PUT/PATCH | `/api/v1/products/{id}/` | Token | Update product |
| DELETE | `/api/v1/products/{id}/` | Token | Delete product |
| GET | `/api/schema/` | Public | OpenAPI schema |
| GET | `/api/docs/` | Public | Swagger UI |

## Product Query Features

```text
/api/v1/products/?search=laptop
/api/v1/products/?ordering=price
/api/v1/products/?ordering=-created_at
/api/v1/products/?stock=10
/api/v1/products/?page=2&page_size=20
```

## Curl Examples

Register:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","email":"demo@example.com","password":"StrongPass123!","password_confirm":"StrongPass123!"}'
```

Login:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"StrongPass123!"}'
```

Create product:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/products/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{"name":"Laptop","description":"Developer workstation","price":"1299.99","stock":5}'
```

List/search products:

```bash
curl "http://127.0.0.1:8000/api/v1/products/?search=laptop&ordering=price&page_size=5"
```

Profile:

```bash
curl http://127.0.0.1:8000/api/v1/auth/profile/ \
  -H "Authorization: Token YOUR_TOKEN"
```

## Example Responses

Register response:

```json
{
  "success": true,
  "message": "User registered successfully.",
  "data": {
    "user": {
      "id": 1,
      "username": "demo",
      "email": "demo@example.com",
      "first_name": "",
      "last_name": "",
      "date_joined": "2026-05-29T00:00:00Z"
    },
    "token": "abc123"
  },
  "errors": null
}
```

Paginated product list response:

```json
{
  "success": true,
  "message": "Results retrieved.",
  "data": {
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "name": "Laptop",
        "description": "Production-grade developer laptop.",
        "price": "1299.99",
        "stock": 12,
        "created_at": "2026-05-29T00:00:00Z",
        "updated_at": "2026-05-29T00:00:00Z"
      }
    ]
  },
  "errors": null
}
```

Validation error response:

```json
{
  "success": false,
  "message": "Request failed",
  "data": null,
  "errors": {
    "price": ["Price must be greater than zero."]
  }
}
```

## Tests

```powershell
python manage.py test apps.authentication apps.products
```

## Postman

Import `postman_collection.json`, run `Register` or `Login`, then set the returned token as the `token` collection variable.
