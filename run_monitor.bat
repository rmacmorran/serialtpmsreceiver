@echo off
echo TPMS Serial Monitor Quick Start
echo ==============================
echo.
echo Available COM ports:
powershell -Command "Get-CimInstance -Class Win32_SerialPort | Select-Object DeviceID, Description | Format-Table -AutoSize"
echo.
echo Usage examples:
echo   python tpms_monitor.py COM20
echo   python tpms_monitor.py COM20 -b 19200
echo   python tpms_monitor.py COM20 -l tpms_log.txt
echo.
echo Press any key to exit...
pause >nul
