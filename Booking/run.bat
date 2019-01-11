@echo off                           //Turn off screen text messages
:loop                               //Set marker called loop, to return to
python booking.py
timeout /t 600 >null               //Wait 20 minutes
(optional)
goto loop
