@echo off
REM -------- CONFIGURATION ----------
set FILE_NAME=apps.py
set ICON_PATH=logo.ico
set OUTPUT_DIR=dist
set EXE_NAME=Wiibrlyt
REM ---------------------------------

echo 🔄 Nettoyage des anciens fichiers temporaires...
if exist %FILE_NAME%.onefile-build (
    rmdir /s /q %FILE_NAME%.onefile-build
)

if exist %FILE_NAME%.build (
    rmdir /s /q %FILE_NAME%.build
)

if exist %OUTPUT_DIR% (
    echo 🧹 Suppression de l'ancien dossier %OUTPUT_DIR%...
    rmdir /s /q %OUTPUT_DIR%
)

echo 🚀 Compilation de %FILE_NAME% avec Nuitka...
python -m nuitka ^
    --mingw64 ^
    --onefile ^
    --follow-imports ^
    --enable-plugin=pyqt5 ^
    --windows-disable-console ^
    --windows-icon-from-ico=%ICON_PATH% ^
    --output-filename=%EXE_NAME%.exe ^
    --output-dir=%OUTPUT_DIR% ^
    %FILE_NAME%

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Échec de la compilation.
    pause
    exit /b 1
)

echo ✅ Compilation réussie !
echo 📁 Fichier final : %OUTPUT_DIR%\%EXE_NAME%.exe
pause
