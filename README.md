# SETUP TO RUN THE DJANGO PROJECT VIA DOCKER COMPOSE

# Klarian Query Engine

## Overview

This project is a Django application that allows users to upload and filter data from JSON and CSV files. The application uses PostgreSQL as the database, and Docker for containerization.
Please make sure you have installed docker and made a set up on your machine. 

## Steps to Test the Application

### Step 1: Clone the Project

Open your command prompt and clone the project to your desired folder using the following command:
```sh
git clone https://github.com/karthick0502/klarian.git
```

### Step 2: Navigate to the Project Directory

Change to the project directory:
```sh
cd klarian
```
Here you will find all the project files, including the `Dockerfile` and `docker-compose.yml` file.

### Step 3: Build and Start the Docker Containers

Run the following command to build and start the Docker containers:
```sh
docker-compose up -d --build
```

**Explanation**: This command performs the following operations:
- Builds the Docker image for the Django application.
- Creates and starts the PostgreSQL container (`postgres_db`) and the Django application container (`MySuperDataCompanyInc`).
- The PostgreSQL container is initialized with the database `mysuperdata`, user `mysuperdatauser`, and password `mysuperdatapassword`.
- The Django application container is started and the application runs on `localhost:8000`.

### Step 4: Migrate the Django Models

After starting the containers, you need to migrate the Django models. This operation is required the first time you run the containers because the PostgreSQL database is pulled directly from Docker Hub and needs to be set up.
```sh
docker-compose exec djangoapp python manage.py migrate
```

### Step 5: Test the Application

Open your browser and navigate to `http://localhost:8000`. You will find two URL endpoints:
- `http://localhost:8000` - File upload
- `http://localhost:8000/filter/` - Filter data from the uploaded file content

**Samples**: Some sample input files are provided to upload in the project directory.

**File Upload**: The home URL (`http://localhost:8000`) takes you to the file upload screen. You can upload JSON or CSV files here. If you try to upload other file types, the application will not allow it.

**Filter Data**: After uploading, you will be redirected to the second URL (`http://localhost:8000/filter/`), where you can see all the data from the uploaded file. Use the search box to find specific data records. 

orelse filter the data by parsing filter parameter called type in the url endpoints,

1. Open your web browser and navigate to the following URL: (`http://localhost:8000/filter/?type=<search_data>`) Replace `<search_data>` with the term you want to search for in the dataset.

2. For example, if you want to filter records containing the word 'coffee', use: (`http://localhost:8000/filter/?type=coffee`)

3. If the entered search data matches any records in the dataset, only those records will be displayed. If no matching records are found, an empty result set will be returned.

### Step 6: Get Data as JSON

You can test the API endpoints to get data in JSON format using Postman or the command line.

**Using Postman**:
1. Enter the URL `http://localhost:8000/filter/`.
2. Add the header `Accept: application/json`.
3. Send the GET request to receive the response in JSON format.

**Using Curl**:
```sh
curl -X GET http://localhost:8000/filter/ -H "Accept: application/json"
```

### Step 7: Check Database Records

To verify how the PostgreSQL database stores the files, enter the PostgreSQL container and query the data:
```sh
docker exec -it postgres_db bash
```
Once inside the container, run:
```sh
PGPASSWORD=mysuperdatapassword psql -U mysuperdatauser -d mysuperdata
```
To see all the tables:
```sql
\dt
```
To query the data:
```sql
SELECT * FROM dataapp_uploadedfile;
SELECT * FROM dataapp_filedata;
```

### Step 8: stop the running Docker Containers

Run the following command to stop the Docker containers:
```sh
docker-compose down
```
If you have any questions or encounter any issues, feel free to open an issue on the [GitHub repository](https://github.com/karthick0502/klarian/issues).
