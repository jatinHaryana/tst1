import os
import subprocess
from flask import Flask, request, jsonify
from pyngrok import ngrok

# Flask app initialization
app = Flask(__name__)

# Replace this with your ngrok auth token
NGROK_AUTH_TOKEN = "2qnNYGSJC9Rg37qD1d6fjFldlDD_5hZPJw7mFh1mZQUUHJaKS"  # Replace with your auth token
BINARY_PATH = "./Spike"  # Path to the binary you want to execute

# Authenticate and start ngrok
ngrok.set_auth_token(NGROK_AUTH_TOKEN)
public_url = ngrok.connect(5000)
print(f" * ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:5000\"")

# Save the ngrok public URL to a .txt file
with open("ngrok_url.txt", "w") as file:
    file.write(str(public_url))
print("Ngrok public URL saved to ngrok_url.txt")

@app.route('/run_binary', methods=['POST'])
def run_binary():
    try:
        # Extract parameters from the request payload
        data = request.get_json()
        ip = data.get("ip")
        port = data.get("port")
        duration = data.get("time")
        packet_size = data.get("packet_size")
        threads = data.get("threads")

        # Validate input parameters
        if not all([ip, port, duration, packet_size, threads]):
            return jsonify({"error": "Missing required parameters: ip, port, time, packet_size, threads"}), 400

        # Log incoming request
        print(f"Request received: IP={ip}, Port={port}, Time={duration}, Packet Size={packet_size}, Threads={threads}")

        # Execute the binary with the extracted parameters
        result = subprocess.run(
            [BINARY_PATH, ip, str(port), str(duration), str(packet_size), str(threads)],
            capture_output=True,
            text=True
        )

        # Return the result of the binary execution
        return jsonify({
            "output": result.stdout.strip(),
            "error": result.stderr.strip() if result.stderr else None
        })

    except Exception as e:
        return jsonify({"error": f"Failed to process request: {str(e)}"}), 500

if __name__ == '__main__':
    print(f"Server running at public URL: {public_url}/run_binary")
    app.run(port=5000, debug=True)
    