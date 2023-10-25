@echo off
setlocal

:loop
python "C:\Users\Alessandro\test.py" 
timeout /t 1800  # Espera 30 min (1800 segundos)
goto :loop
