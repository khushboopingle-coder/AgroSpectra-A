@echo off
echo ========================================================
echo           Starting AgroSpectra AI Application
echo ========================================================
echo.
REM Attempt using Python 3.11 where tensorflow and keras are installed
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Launching with Python 3.11 launcher...
    py -3.11 -m streamlit run app.py
) else (
    echo Launching with default Python streamlit...
    streamlit run app.py
)
pause
