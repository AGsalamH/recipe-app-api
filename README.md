# Recipe API
### Introduction
The Recipe API is a RESTful service built using `Django` and `Django REST Framework`. It allows users to create, store, and manage recipes, tags, and ingredients. The API uses `token-based` authentication to secure endpoints and `PostgreSQL` as the main database.

---
### Getting Started
Prerequisites:

You don't have to install all dependencies on your machine.

All you need to do is to make sure that **`Docker`** is already installed on your machine.

---

### **Installation**

1. **Clone the repository:**

    ```bash
    git clone https://github.com/AGsalamH/recipe-app-api.git
    cd recipe-api

    ```

2. **Build docker Image:**
    
    ```bash
    docker-compose build .
    ```

3. **Create a superuser:**

    ```bash
    docker-compose run --rm django sh -c "python manage.py createsuperuser"    
    ```

4. **Run the development server:**

    ```bash
    docker-compose up
    ```
## **Authentication**

This API uses token-based authentication. To access most endpoints, you need to include a token in your requests.

### **Obtain Token**

To get a token, send a POST request to **`/users/auth-token/`** with your email and password:

```bash
POST /api/token/

```

**Request Body:**

```json
{
  "email": "youremail",
  "password": "yourpassword"
}

```

**Response:**

```json
{
  "token": "yourtoken"
}

```

### **Use Token**

Include the token in the **`Authorization`** header of your requests:

```http
Authorization: Token yourtoken

```

## **Endpoints Overview**

- **Recipes**
    - **`GET /api/recipes/`** - List all recipes
    - **`POST /api/recipes/`** - Create a new recipe
    - **`GET /api/recipes/{id}/`** - Retrieve a specific recipe
    - **`PUT /api/recipes/{id}/`** - Update a specific recipe
    - **`DELETE /api/recipes/{id}/`** - Delete a specific recipe

- **Ingredients**
    - **`GET /api/ingredients/`** - List all ingredients
    - **`POST /api/ingredients/`** - Create a new ingredient
    - **`GET /api/ingredients/{id}/`** - Retrieve a specific ingredient
    - **`PUT /api/ingredients/{id}/`** - Update a specific ingredient
    - **`DELETE /api/ingredients/{id}/`** - Delete a specific ingredient

- **Tags**
    - **`GET /api/tags/`** - List all tags
    - **`POST /api/tags/`** - Create a new tag
    - **`GET /api/tags/{id}/`** - Retrieve a specific tag
    - **`PUT /api/tags/{id}/`** - Update a specific tag
    - **`DELETE /api/tags/{id}/`** - Delete a specific tag

