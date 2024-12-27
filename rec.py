import os
import subprocess
from flask import Flask, request, jsonify
from pyngrok import ngrok

app = Flask(__name__)

# Set your ngrok auth token
NGROK_AUTH_TOKEN = "2qn8Ntk22rmZG3VkcmaVKPmltQP_2beoER7DLX8svQ6UtLRud"  # Replace with your token
ngrok.set_auth_token(NGROK_AUTH_TOKEN)

# Start ngrok tunnel
public_url = ngrok.connect(5000)
print(f" * ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:5000\"")

# Save the ngrok public URL to a .txt file
with open("ngrok_url.txt", "w") as file:
    file.write(str(public_url))
print("Ngrok public URL saved to ngrok_url.txt")

@app.route('/run_Spike', methods=['POST'])
def run_spike():
    try:
        # Extract parameters from JSON request
        data = request.get_json()
        ip = data.get("ip")
        port = data.get("port")
        duration = data.get("time")
        packet_size = data.get("packet_size")
        threads = data.get("threads")

        # Validate inputs
        if not all([ip, port, duration, packet_size, threads]):
            return jsonify({"error": "Missing required parameters (ip, port, time, packet_size, threads)"}), 400

        # Run the Spike binary with provided parameters
        result = subprocess.run(
            ["./Spike", ip, str(port), str(duration), str(packet_size), str(threads)],
            capture_output=True, text=True
        )

        # Return output and error from Spike binary
        return jsonify({
            "output": result.stdout.strip(),
            "error": result.stderr.strip() if result.stderr else None
        })

    except Exception as e:
        return jsonify({"error": f"Failed to run Spike: {str(e)}"}), 500

if __name__ == '__main__':
    print(f"Server running at public URL: {public_url}/run_spike")
    app.run(port=5000, debug=True)
    
