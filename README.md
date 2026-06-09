#  Bounce Arena – Browser Permission Security Demo

A cyberpunk-themed browser game built using Flask, JavaScript, HTML5 Canvas, Geolocation API, and Camera API.

This project demonstrates how browser permission systems work in modern web applications through a real-time arcade game interface.

---

#  DISCLAIMER

This project is created strictly for:

- Educational purposes
- Cybersecurity awareness
- Browser API learning
- Ethical testing environments

The application requests permissions directly from the browser.  
Users must manually allow camera and location access before any data is used.

Do NOT use this project without user consent.

---

#  FEATURES

-  Real-time Geolocation API
-  Camera API Integration
-  Cloudflare Tunnel Support
-  Flask Backend
-  Automatic Data Logging
-  Image Capture Support
-  Mobile Friendly Controls
-  Real-time Score System

---

# TECHNOLOGIES USED

- Python3
- Flask
- HTML5 Canvas
- JavaScript
- CSS3
- Cloudflare Tunnel
- Browser Geolocation API
- Browser MediaDevices API

---

# PROJECT STRUCTURE

```bash
quizgame/
│
├── app.py
├── captured_data/
│
├── requirements.txt
└── README.md
```

---

#  REQUIREMENTS

Install these before running the project:

##  Python Packages

```bash
pip install flask requests opencv-python
```

OR

Create a requirements.txt file:

```txt
flask
requests
opencv-python
```

Then install:

```bash
pip install -r requirements.txt
```

---

#  CLOUDFLARED INSTALLATION

Download Cloudflared:

## Linux (Kali)

```bash
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
```

Rename:

```bash
mv cloudflared-linux-amd64 cloudflared
```

Give Permission:

```bash
chmod +x cloudflared
```

---

#  SETUP & RUN

## 1️ Clone Repository

```bash
git clone https://github.com/harpind3r/Get-location.git
```

---

## 2️ Open Project Folder

```bash
cd quizgame
```



---

## 3️ Install Dependencies

```bash
pip install -r requirements.txt
```

---

#  START FLASK SERVER

Run:

```bash
python3 app.py
```
<img width="800" height="500" alt="Screenshot (344)" src="https://github.com/user-attachments/assets/9810a037-b29f-4d70-a7be-ec1ee50981e3" />

You should see:

```bash
Running on http://127.0.0.1:5000
```


---

#  START CLOUDFLARE TUNNEL

Open SECOND terminal.

Run:

```bash
./cloudflared tunnel --url http://localhost:5000
```




Example Output:

```bash
https://random-name.trycloudflare.com
```
<img width="800" height="500" alt="Screenshot (345)" src="https://github.com/user-attachments/assets/a0532092-f07e-42b2-b219-1f284018a258" />



Open that link in browser.

---

#  HOW IT WORKS

1. User opens game link
2. Browser requests:
   - Location Permission
   - Camera Permission
3. After permission approval:
   - Game starts
   - Score tracking begins
   - Browser API data is processed
4. Backend logs:
   - Username
   - Score
   - Timestamp
   - Coordinates
   - Accuracy
   - Captured image

---
 

#  EDUCATIONAL CONCEPTS

This project demonstrates:

- Flask Backend Development
- Browser Permission Systems
- Geolocation API
- MediaDevices API
- Canvas Game Development
- Cloudflare Tunnel Usage
- Frontend + Backend Integration
- Ethical Security Demonstration

---

#  COMMANDS SUMMARY

## Start Project

```bash
cd quizgame
python3 app.py
```

---

## Start Cloudflare Tunnel

```bash
./cloudflared tunnel --url http://localhost:5000
```

---

#  SCREENSHOTS

## Login Screen
 <img width="1000" height="700" alt="Screenshot 2026-06-09 222731" src="https://github.com/user-attachments/assets/21501c5b-fe64-4d2c-8292-c6a8b1ef7dc7" />


---

## Gameplay
<img width="1000" height="700" alt="Screenshot 2026-06-09 222755" src="https://github.com/user-attachments/assets/716030de-198e-48e8-88e5-9dbfb577b2e6" />

 

---

## Game Over

<img width="1000" height="700" alt="Screenshot 2026-06-09 222805" src="https://github.com/user-attachments/assets/2e192e04-78fa-406f-987b-ee3f2d94e184" />


---

#  LICENSE

MIT License

---

# AUTHOR

Created by Harpind3r

Cybersecurity | Browser API Research | Flask Development

---

# GITHUB DESCRIPTION

```txt
Cyberpunk browser game demonstrating Geolocation API, Camera API, Flask backend logging, and Cloudflare Tunnel integration.
```

---

# 🏷 TAGS

```txt
python flask javascript cybersecurity geolocation-api camera-api cloudflare-tunnel html5-canvas browser-security ethical-hacking
```
