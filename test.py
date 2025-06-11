import requests
import sys

def test_backend():
    try:
        # Test root endpoint
        response = requests.get('http://localhost:8000/')
        print("Root endpoint test:", response.status_code)
        print("Response:", response.json())
        
        # Test products endpoint
        response = requests.get('http://localhost:8000/products/')
        print("\nProducts endpoint test:", response.status_code)
        print("Response:", response.json())
        
        # Test cart endpoint
        response = requests.get('http://localhost:8000/cart/user123')
        print("\nCart endpoint test:", response.status_code)
        print("Response:", response.json())
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the backend server.")
        print("Make sure the server is running on http://localhost:8000")
        sys.exit(1)
    except Exception as e:
        print("Error:", str(e))
        sys.exit(1)

if __name__ == "__main__":
    test_backend() 