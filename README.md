# Jewellery Shop Backend

This is the backend API for the Jewellery Shop, built with FastAPI and using MongoDB as the database. It provides RESTful endpoints for CRUD operations on jewellery products.

## Features

*   **Product Management:** API endpoints for creating, reading, updating, and deleting (CRUD) jewellery products.
*   **MongoDB Integration:** Uses PyMongo to interact with a MongoDB database.
*   **CORS Enabled:** Configured to allow requests from the frontend application.

## Technologies Used

*   **FastAPI:** A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
*   **Uvicorn:** An ASGI server for running FastAPI applications.
*   **PyMongo:** A Python distribution containing tools for working with MongoDB.
*   **python-dotenv:** For loading environment variables from a `.env` file (e.g., MongoDB connection string).
*   **MongoDB:** A NoSQL document database.

## Setup and Running

Follow these steps to get the backend API up and running on your local machine.

### Prerequisites

*   Python 3.7+
*   pip (Python package installer)
*   MongoDB instance (local or MongoDB Atlas)

### Installation

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
2.  **Create and activate a virtual environment (recommended):**
    *   **Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\Activate
        ```
    *   **macOS/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### MongoDB Configuration

1.  Ensure you have a running MongoDB instance (local or cloud).
2.  **Option 1: Local MongoDB**
    *   If running locally, the default connection string `mongodb://localhost:27017/` is used.
3.  **Option 2: MongoDB Atlas (or remote)**
    *   Create a `.env` file in the `backend/` directory.
    *   Add your MongoDB connection string to it:
        ```
        MONGO_URL="mongodb+srv://<username>:<password>@<cluster-url>/<dbname>?retryWrites=true&w=majority"
        ```
        (Remember, the `.env` file is in `.gitignore` and should not be pushed to public repositories).

### Running the API Server

1.  **Start the backend API:**
    *   Ensure your virtual environment is activated.
    ```bash
    uvicorn main:app --reload
    ```
2.  The API will typically be accessible at `http://127.0.0.1:8000`.
3.  You can access the interactive API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`. Use this to test the endpoints and add/manage products.

### Endpoints

*   `POST /products/`: Add a new product.
*   `GET /products/`: Retrieve all products.
*   `PUT /products/{name}`: Update a product by name.
*   `DELETE /products/{name}`: Delete a product by name.
