@echo off
chcp 65001 >nul
echo ========================================
echo    Metis Homeland Map V5 - Local Server
echo ========================================
echo.
echo This script starts the map server using WSL.
echo.

:: Get WSL IP for direct access
for /f "tokens=2 delims=[]" %%a in ('wsl hostname -I 2^>nul') do set WSLIP=%%a
if defined WSLIP (
    echo WSL IP: %WSLIP%
)

:: Start server in WSL using serve.py (has CORS headers)
echo Starting server...
start "HomelandMap Server" cmd /k "wsl python3 -c ""cd /mnt/c/Users/Bayard%%20deVries/Desktop/HomelandMap && python3 serve.py 8888"""

:: Wait for server
timeout /t 3 /nobreak >nul

:: Try localhost
curl -s -o nul -w "%%{http_code}" http://localhost:8888/ 2>nul
if errorlevel 1 (
    echo.
    echo WARNING: Could not verify localhost connection.
    echo Try these URLs in your browser:
    echo   http://localhost:8888
    echo   http://%WSLIP%:8888
) else (
    echo Server started on http://localhost:8888
)

:: Open browser
start http://localhost:8888

echo.
echo Close the server window to stop.
pause