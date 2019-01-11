@echo off                           
:loop                               
python booking.py

timeout /t 600 /nobreak
goto loop
