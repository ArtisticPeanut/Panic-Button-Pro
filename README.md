

# 🚨 PushPulse: Guardian Alert System

**PushPulse** is a personal safety alert system designed for immediate, discreet distress signaling to a predefined "Safe Circle" and a centralized security dispatch. It uses a Flask backend for centralized management and the Pushbullet API for reliable, cross-platform notifications.

The system is activated by a **long-press** on a mobile-optimized web interface, which sends real-time location data to designated guardians and security personnel.

## ✨ Features

  * **Long-Press Activation:** A 1.5-second press-and-hold mechanism prevents accidental triggering and provides visual feedback.
  * **Dual Notification System:**
      * **Guardians:** Sends immediate Pushbullet notifications to a predefined list of trusted email addresses with a direct Google Maps link to the student's location.
      * **Security Dispatch:** Pushes a critical alert to a dedicated Pushbullet channel, directing staff to a real-time dashboard.
  * **High-Accuracy GPS:** Attempts to retrieve the most precise location data, including a retry mechanism if initial accuracy is poor.
  * **Centralized Dashboard (WIP):** Includes an endpoint (`/dashboard`) for security staff to view and resolve active alerts.
  * **Simple Resolution:** Alerts can be manually resolved via a dedicated API endpoint (`/resolve_alert/<student_id>`).

## 🛠️ Project Structure

The system is composed of two main files:

  * `brain.py`: The core backend logic built with Flask. Handles API endpoints, location processing, and Pushbullet communication.
  * `client.html`: The mobile-optimized front-end interface, containing the long-press button logic and GPS retrieval scripts.

## ⚙️ Installation and Setup

### 1\. Prerequisites

  * Python 3.x
  * A Pushbullet Account and API Key
  * The following Python packages: `Flask`, `requests`

### 2\. Configure Pushbullet

1.  **Get Your API Key:** Log in to Pushbullet, go to **Settings \> Account**, and copy your **Access Token**.
2.  **Create a Dispatch Channel:** Create a new Pushbullet channel (e.g., named "Security Dispatch"). Note the **Channel Tag** (e.g., `securitydispatch`).

### 3\. Install Dependencies

```bash
pip install flask requests
```

### 4\. Update Configuration (`brain.py`)

Open `brain.py` and modify the following configuration variables:

| Variable | Description |
| :--- | :--- |
| `PUSHBULLET_API_KEY` | **Paste your Pushbullet Access Token here.** |
| `DISPATCH_CHANNEL_TAG` | **Enter your Pushbullet channel tag here.** |
| `student_guardians` | Define your student IDs and their corresponding list of guardian emails. |
| `student_names` | Define your student IDs and their full names. |

### 5\. Run the Server

Execute the main Python script:

```bash
python brain.py
```

The server will start on `http://0.0.0.0:5000`.

## 🚀 Usage

### 1\. Student Client Activation

1.  Access the client interface: **`http://<your-server-ip>:5000/`** (or use the student ID endpoint like `http://<your-server-ip>:5000/S12345`).
2.  On a mobile device, **press and hold** the red **EMERGENCY ALERT** button for 1.5 seconds.
3.  The system will attempt to get a precise GPS location and send the alert.

### 2\. Security Dispatch Monitoring

  * **Dashboard (WIP):** Access the basic dashboard page: **`http://<your-server-ip>:5000/dashboard`**
  * **API Data:** Real-time active alerts can be queried via the API: **`http://<your-server-ip>:5000/alert_status`**

### 3\. Resolving an Alert

Once an incident is resolved, the alert must be cleared from the system using the dedicated API endpoint:

```http
POST /resolve_alert/<student_id>
```

**Example (to resolve alert for student S12345):**

```bash
curl -X POST http://<your-server-ip>:5000/resolve_alert/S12345
```

## 🗺️ Note on Map Links

The `brain.py` script constructs a static Google Maps URL for the Guardian notifications:

```python
map_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"
```

This is a placeholder and should be updated to a standard Google Maps URL format for optimal delivery:

```python
map_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"
```

## 💡 Potential Enhancements

  * **Database Integration:** Replace in-memory dictionaries (`active_alerts`, `student_guardians`) with SQLite, PostgreSQL, or MongoDB.
  * **Web Dashboard:** Complete the `dashboard.html` implementation to visually plot active alerts on a map (e.g., using Leaflet or Google Maps API).
  * **SMS/Call Fallback:** Integrate a service like Twilio to ensure critical alerts are received even if guardians don't have Pushbullet installed.
  * **Heartbeat/Check-in:** Implement a feature for students to regularly check-in, allowing the system to detect unresponsiveness.
