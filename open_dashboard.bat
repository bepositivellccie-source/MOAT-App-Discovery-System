@echo off
cd /d "%~dp0"
echo Demarrage du serveur AppHunter sur http://localhost:8080 ...
start "" http://localhost:8080/dashboard_live.html
python scripts/serve.py 8080
