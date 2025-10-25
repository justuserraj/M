from flask import Flask, request
import threading
import queue
import sys
from flask_cors import CORS

# A shared queue to pass commands from the server to the main program
command_queue = queue.Queue()

app = Flask(__name__)
CORS(app) # Enables CORS for all routes

@app.route('/command', methods=['POST'])
def receive_command():
    try:
        data = request.json
        command = data.get('command')
        if command:
            print(f"Received command from phone: {command}")
            command_queue.put(command)
            return {"status": "success", "message": "Command received"}, 200
        else:
            return {"status": "error", "message": "No command provided"}, 400
    except Exception as e:
        print(f"Error receiving command: {e}")
        return {"status": "error", "message": "An error occurred"}, 500

def run_server():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    
    print(f"Server running. Connect your phone to: http://{local_ip}:5000")
    
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    print("Server is running in a separate thread. This script does nothing else.")
    try:
        while True:
            command = command_queue.get()
            print(f"Main program received command from queue: {command}")
            # Here, you would call your main program's command handling logic
    except KeyboardInterrupt:
        print("Shutting down.")
        sys.exit()