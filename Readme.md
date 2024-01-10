# Project Overview

This project involves creating a microservices-based application using Docker to run each microservice in a reproducible environment.

## Functionality

The application allows users to upload photos, automatically tag them, and store them in a designated folder. Simultaneously, a database is created to store all relevant information, including paths to images and assigned tags. This information is utilized to facilitate image searches based on specific tags.

## Microservices

### 1. API Microservice

- **Implementation**: Flask
- **Server**: Waitress

### 2. Database Microservice

- **Database**: MySQL 8.0

## Getting Started

To run the application locally, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/mgranica/M02-arquitecturas_transaccionales-proyecto_consolidacion.git
    ```

2. Navigate to the project directory:

    ```bash
    cd project-directory
    ```

3. Create and activate virtual environment
  
    ```
    python -m venv venv
    source venv/bin/activate      # On Unix/Linux
    # or
    .\venv\Scripts\activate       # On Windows

    ```

4. Install the required dependencies:
    ```bash
    python -m pip install -r app/requirements.txt
    ```

5. Set up API credentials
  * create the file `/app/credentials.json` to set the apis credentials. you can use the template provided below:
    ```json
    {
    "imagga": {
        "password": "YOUR_PASSWORD",
        "api_key": "YOUR_API_KEY",
        "api_secret": "YOUR_API_SECRET",
        "image_url": ""
    },
    "imagekit": {
        "public_key": "YOUR_PUBLIC_KEY",
        "private_key":"YOUR_PRIVATE_KEY",
        "url_endpoint": "YOUR_END_POINT",
        "password": "YOUR_PASSWORD"
    }
    }
    ```

6. Set up Docker environment:

    ```bash
    docker-compose up
    ```

7. Access Adminer for database management at `http://localhost:8080`:
  * **Server**: Use db_container as the database server name.
  * **Username/Password**: Check your *docker-compose.yml* for the MySQL credentials.

8. Interact with the API using the provided Jupyter notebook:
  * Open notebooks/API_CALL.ipynb in Jupyter.
  * Follow the instructions in the notebook to make API calls and explore functionalities.

## API Endpoints

### Image Upload

- **Endpoint**: `/images`
- **Method**: POST
- **Description**: Upload a photo, and the API will automatically tag and store it.
- **Input**:
  - JSON body with a base64-encoded image (data).
  - Optional query parameter min_confidence (default: 80).
- **Response**: JSON with image datails and tags

### Search Images

- **Endpoint**: `/images`
- **Method**: GET
- **Description**: Retrieve images with a specific tag.
- **Filters**: `min_date`, `max_date`, and `tags` as query parameters.
- **Response**: List of images with details and associated tags based on filters.

### Search Image

- **Endpoint**: `/images/<picture_id>`
- **Method**: GET
- **Description**: Retrieve images with a specific tag.
- **Input**: Image ID as a path parameter.
- **Response**: JSON with details of a specific image and associated tags.

### Search Tags

- **Endpoint**: `/tags`
- **Method**: GET
- **Description**: Retrieve tags with aggregations.
- **Filters**: `min_date`, `max_date` as query parameters.
- **Response**: List of tags with the number of associated images and confidence statistics.


# Database Schema

We will use a MySQL version 8.0 database. Explore the image documentation on [dockerhub](https://hub.docker.com/_/mysql). Follow these steps:

- Use a database named `Pictures`.
- Use a user with the name `mbit` and password `mbit`.

The data model to be used is as follows:

## Table `pictures`

Table containing a row for each image stored in the system. It has the following columns:

- `id`: String column (36 characters) corresponding to a unique uuid for each image. It is the **Primary Key**.
- `size`: Integer indicating the amount of space occupied by the image.
- `path`: String identifying the path where the image is stored.
- `date`: String identifying the date the image was created, in `YYYY-MM-DD HH:MM:SS` format.

## Table `tags`

Table containing tags associated with each image. It has the following columns:

- `tag`: Tag name associated with the image (up to 32 characters).
- `picture_id`: Uuid of the image associated with the tag. It is a **Foreign Key**.
- `confidence`: Confidence level of the tag associated with the image.
- `date`: String identifying the date the image was created, in `YYYY-MM-DD HH:MM:SS` format.

The **Primary Key** is composed of the `tag` and `picture_id` columns.

## Next Steps

To enhance and extend the functionality of the application, consider the following steps:

1. **Implement User Authentication**: Secure the API endpoints with user authentication to control access.

2. **Provide initial content to DB**: include syntetic data to populate the database 

3. **Implement new functionalities**: complete the CRUD system by adding DELETE & UPDATE by <picture_id>.

4. **Improve Error handling**: make more robust validations, include to POST request, duplicated images interruption. (Currently the id is randmized however the same image can have multiples ids). 

4. **Frontend Integration**: Develop a user-friendly frontend to interact with the API and display images with tags.

5. **Docker Swarm/Kubernetes Deployment**: Explore deploying the application using Docker Swarm or Kubernetes for better scalability and management.

Feel free to contribute and make improvements to the project. If you encounter any issues, please open a new GitHub issue. Happy coding!
