from flask import Flask, request, jsonify, render_template
import requests
import time

app = Flask(__name__)

# --- CONFIGURATION ---
PUSHBULLET_API_KEY = "YOUR_API_KEY" # Replace with your key
DISPATCH_CHANNEL_TAG = "securitydispatch" # Create a Pushbullet channel for security

# Simple in-memory storage for active alerts (Replace with a database for production)
active_alerts = {}
# Simple dictionary for Guardian mapping (Replace with a database)
student_guardians = {
    "S12345": ["example1@gmail.com", "example2@gmail.com", "example3@gmail.com","example4@gmail.com","example5@gmail.com"],
    "S67890": ["example6@gmail.com"],
}
student_names = {
    "S12345": "John Doe",
    "S67890": "Doe John",
}
# ---------------------

def send_pushbullet_notification(email_or_channel, title, body, url=None):
    """Sends a push notification using the Pushbullet API."""
    headers = {'Access-Token': PUSHBULLET_API_KEY}
    data = {
        "type": "link" if url else "note",
        "title": title,
        "body": body,
    }
    if url:
        data["url"] = url
    
    if "@" in email_or_channel:
        data["email"] = email_or_channel # Send to a specific Guardian email
    else:
        data["channel_tag"] = email_or_channel # Send to the Dispatch channel

    try:
        response = requests.post("https://api.pushbullet.com/v2/pushes", headers=headers, json=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending Pushbullet notification: {e}")

@app.route('/activate_alert', methods=['POST'])
def activate_alert():
    """Endpoint for the student client to send an emergency alert."""
    data = request.json
    student_id = data.get('student_id')
    lat = data.get('latitude')
    lng = data.get('longitude')
    
    if not all([student_id, lat, lng]):
        return jsonify({"status": "error", "message": "Missing data"}), 400

    student_name = student_names.get(student_id, "Unknown Student")
    current_time = time.strftime("%H:%M:%S")
    
    # 1. Update active alerts storage
    active_alerts[student_id] = {'lat': lat, 'lng': lng, 'time': current_time, 'name': student_name}
    
    # 2. Generate Google Maps link for the current location
    map_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"
    
    # 3. Send Alert to Campus Security Dispatch Channel
    dispatch_title = f"🚨 CRITICAL GAS ALERT: {student_name} ({student_id})"
    dispatch_body = f"Student activated alert at {current_time}. Click to view on map dashboard."
    send_pushbullet_notification(DISPATCH_CHANNEL_TAG, dispatch_title, dispatch_body, url=request.host_url + 'dashboard')

    # 4. Send Alerts to Guardians
    guardians = student_guardians.get(student_id, [])
    for email in guardians:
        guardian_title = f"⚠️ {student_name} Needs Help NOW!"
        guardian_body = f"URGENT: {student_name} activated a safety alert at {current_time}. Click for their current location."
        send_pushbullet_notification(email, guardian_title, guardian_body, url=map_link)
    
    print(f"Alert activated for {student_id} at {lat},{lng}")
    return jsonify({"status": "success", "message": "Alert activated and notifications sent."})

@app.route('/alert_status', methods=['GET'])
def get_alert_status():
    """Endpoint for the Dispatch Dashboard to pull real-time alert data."""
    # Return all active alerts
    return jsonify(active_alerts)

@app.route('/resolve_alert/<string:student_id>', methods=['POST'])
def resolve_alert(student_id):
    """Endpoint to manually resolve an alert."""
    if student_id in active_alerts:
        del active_alerts[student_id]
        return jsonify({"status": "success", "message": f"Alert for {student_id} resolved."})
    return jsonify({"status": "error", "message": f"Alert for {student_id} not found."}), 404

@app.route('/')
def student_client():
    """Serves the student's activation page."""
    # Example student ID for testing (replace with actual authentication/token logic)
    return render_template('client.html', student_id="S12345") 

@app.route('/dashboard')
def dispatch_dashboard():
    """Serves the Dispatch Dashboard map view."""
    return render_template('dashboard.html')

if __name__ == '__main__':
    # Use 0.0.0.0 for external access testing
    app.run(host='0.0.0.0', port=5000, debug=True)