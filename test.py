import requests
import webbrowser

# CHANGE THE VARIABLE BELOW TO YOUR FLASK URL
FLASK_URL = "http://localhost:3000"


def http(method, path, data=None):
    print(f"Making {method} request to {FLASK_URL + path}...")
    if method not in ["GET", "POST", "PUT", "DELETE"]:
        raise RuntimeWarning("Invalid method")
    
    if method == "GET":
        response = requests.get(FLASK_URL + path)
    elif method == "POST":
        response = requests.post(FLASK_URL + path, json=data)
    elif method == "PUT":
        response = requests.put(FLASK_URL + path, json=data)
    elif method == "DELETE":
        response = requests.delete(FLASK_URL + path)
    
    print("Received status code:", response.status_code)
    return response

def get(path):
    return http("GET", path)


def post(path, data=None):
    return http("POST", path, data)


def put(path, data=None):
    return http("PUT", path, data)


def delete(path):
    return http("DELETE", path)

def add():
    print("Adding a new product: 'salty nuts' (6.99)")
    post("/api/product/", {"name": "salty nuts", "price": 6.99})
    input("Check for salty nuts in the web page. Press Enter when ready.")
    # webbrowser.open(FLASK_URL + "/products")
    input("Press Enter to continue.")
    print("Adding a new product: 'sweet nuts' (8.99)")
    post("/api/product/", {"name": "sweet nuts", "price": 8.99})
    input("Check for sweet nuts in the web page. Press Enter when ready.")
    # webbrowser.open(FLASK_URL + "/products")
    input("Press Enter to continue.")
    print("Add a new product: 'spicy nuts' (7.99)")
    post("/api/product/", {"name": "spicy nuts", "price": 7.99})
    input("Check for spicy nuts in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/products")
    input("Press Enter to continue.")  
    

def demo():
    input("Press Enter to start the demo.")
    # adding products 
    add()
    #### make orders
    print("Making a new order for 2 salty nuts")
    post("/api/order/", {"customer_id": 1, "items": [{"name": "salty nuts", "quantity": 2}]})
    input("Check for the order in the web page. Press Enter when ready.")
    # webbrowser.open(FLASK_URL + "/orders")
    input("Press Enter to continue.")
    print("Making a new order for 2 sweet nuts")
    post("/api/order/", {"customer_id": 2, "items": [{"name": "sweet nuts", "quantity": 2}]})
    input("Check for the order in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/orders")
    
    
    
    
    

if __name__ == "__main__":
    demo()
