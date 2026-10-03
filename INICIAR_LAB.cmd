@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 goto python
py -3 scripts\check_environment.py
if errorlevel 1 goto fail
py -3 run.py serve
goto end
:python
where python >nul 2>nul
if errorlevel 1 goto missing
python scripts\check_environment.py
if errorlevel 1 goto fail
python run.py serve
goto end
:missing
echo Instala Python 3.10 o posterior. Este lanzador no instala programas.
goto end
:fail
echo Revisa el informe anterior. Si el puerto esta ocupado, cierra el servidor anterior.
:end
pause
endlocal
