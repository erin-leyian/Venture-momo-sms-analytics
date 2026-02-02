"""
MoMo Transactions REST API Server
Simple implementation using http.server with Basic Authentication
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import base64
import os

# Configuration
HOST = "localhost"
PORT = 8000
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dsa", "momo_transactions.json")

# Basic Auth credentials
USERS = {"admin": "admin123", "user": "user123"}


def load_transactions():
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            transactions = {}
            for msg in data.get("messages", []):
                tx_id = msg.get("parsed_transaction", {}).get("transaction_id")
                if tx_id:
                    transactions[tx_id] = msg
            return transactions
    except:
        return {}


def save_transactions(transactions):
    """Save transactions back to JSON file"""
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    data["messages"] = list(transactions.values())
    data["metadata"]["count"] = str(len(transactions))
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


TRANSACTIONS = load_transactions()


def check_auth(auth_header):
    """Validate Basic Authentication header"""
    if not auth_header or not auth_header.startswith("Basic "):
        return False
    try:
        credentials = base64.b64decode(auth_header[6:]).decode()
        username, password = credentials.split(":", 1)
        return USERS.get(username) == password
    except:
        return False


class APIHandler(BaseHTTPRequestHandler):
    
    def send_json(self, status, data):
        """Send JSON response"""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def authenticate(self):
        """Check auth, return True if valid, send 401 if not"""
        if not check_auth(self.headers.get("Authorization")):
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="MoMo API"')
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Unauthorized"}).encode())
            return False
        return True
    
    def get_body(self):
        """Parse JSON body from request"""
        length = int(self.headers.get("Content-Length", 0))
        if length:
            return json.loads(self.rfile.read(length))
        return None
    
    def do_GET(self):
        """GET /transactions or GET /transactions/{id}"""
        if not self.authenticate():
            return
        
        path = self.path.rstrip("/")
        
        if path == "/transactions":
            # GET /transactions - list all
            self.send_json(200, {"transactions": list(TRANSACTIONS.values()), "count": len(TRANSACTIONS)})
        
        elif path.startswith("/transactions/"):
            # GET /transactions/{id}
            tx_id = path.split("/")[-1]
            if tx_id in TRANSACTIONS:
                self.send_json(200, TRANSACTIONS[tx_id])
            else:
                self.send_json(404, {"error": "Transaction not found"})
        else:
            self.send_json(404, {"error": "Not found"})
    
    def do_POST(self):
        """POST /transactions - create new transaction"""
        if not self.authenticate():
            return
        
        if self.path.rstrip("/") != "/transactions":
            self.send_json(400, {"error": "POST only on /transactions"})
            return
        
        body = self.get_body()
        if not body:
            self.send_json(400, {"error": "Missing JSON body"})
            return
        
        tx_id = body.get("parsed_transaction", {}).get("transaction_id")
        if not tx_id:
            self.send_json(400, {"error": "Missing transaction_id"})
            return
        
        if tx_id in TRANSACTIONS:
            self.send_json(409, {"error": "Transaction already exists"})
            return
        
        TRANSACTIONS[tx_id] = body
        save_transactions(TRANSACTIONS)
        self.send_json(201, {"message": "Created", "data": body})
    
    def do_PUT(self):
        """PUT /transactions/{id} - update transaction"""
        if not self.authenticate():
            return
        
        path = self.path.rstrip("/")
        if not path.startswith("/transactions/"):
            self.send_json(400, {"error": "PUT requires /transactions/{id}"})
            return
        
        tx_id = path.split("/")[-1]
        if tx_id not in TRANSACTIONS:
            self.send_json(404, {"error": "Transaction not found"})
            return
        
        body = self.get_body()
        if not body:
            self.send_json(400, {"error": "Missing JSON body"})
            return
        
        TRANSACTIONS[tx_id].update(body)
        save_transactions(TRANSACTIONS)
        self.send_json(200, {"message": "Updated", "data": TRANSACTIONS[tx_id]})
    
    def do_DELETE(self):
        """DELETE /transactions/{id} - delete transaction"""
        if not self.authenticate():
            return
        
        path = self.path.rstrip("/")
        if not path.startswith("/transactions/"):
            self.send_json(400, {"error": "DELETE requires /transactions/{id}"})
            return
        
        tx_id = path.split("/")[-1]
        if tx_id not in TRANSACTIONS:
            self.send_json(404, {"error": "Transaction not found"})
            return
        
        del TRANSACTIONS[tx_id]
        save_transactions(TRANSACTIONS)
        self.send_json(200, {"message": f"Deleted {tx_id}"})


if __name__ == "__main__":
    print(f"Server running on http://{HOST}:{PORT}")
    print(f"Loaded {len(TRANSACTIONS)} transactions")
    print("Auth: admin/admin123 or user/user123")
    
    HTTPServer((HOST, PORT), APIHandler).serve_forever()
