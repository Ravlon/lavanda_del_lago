@echo off

:: CONTROLLA SE ACCESSO DA AMMINISTRATORE!!!
:: Controlla Python

::Setting variables
set ping_error=NESSUNA CONNESSIONE INTERNET TROVATA ******* CONTROLLA CONNESSIONE INTERNET
set internet=[***] Controllo connessione ad Internet...
set git_check=[***] Check 1: Presenza Programma Git
set git_installed=[***]          Git Presente
set python_check=[***] Check 2: Presenza Programma Python
set python_installed=[***]          Python Presente
set git_installation=[***] Installazione di Git
set git_initialised=[***]         Git Inizializzato

set git_id=Git.Git
set python_id=Python.Python.3

set Date_of_backup=%DATE%
set year=%Date_of_backup:~-2%
set day=%Date_of_backup:~0,5%
set month=%day:~-2%
set day=%day:~0,2%
set str_date=%year%.%month%.%day%

:: Check for Backup directory, else create it
if exist .\Backup (cd .) else (md .\Backup)


:: Check Internet Connection
echo %internet%
ping /n 4 www.google.com
if errorlevel 1 (
    echo %ping_error%
    goto :aborted
)

:: Check for Git and Python 3 istallation, if not present install
if exist .\Asset (cd .) else (md .\Asset)
cd .\Asset
if exist %ProgramFiles%\Git (goto :git_end) else (goto :git_init)

:git_end
echo %git_installed%
if exist .\.git (echo %git_initialised%) else (git init)
::PYTHON HOW?


:: Git pull any update of Python Script -> Run Python Script
git pull https://github.com/Ravlon/lavanda_del_lago
python3 Lavanda_del_Lago.py
::move /Y *.csv ..
goto :aborted

:aborted
pause
exit

:git_init
echo %git_installation%
winget install --id %git_id% -e
git init
echo %git_initialised%
goto :git_end