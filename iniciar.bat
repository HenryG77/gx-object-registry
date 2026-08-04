@echo off
echo ========================================
echo   GeneXus Object Registry - Inicio
echo ========================================
echo.

echo IMPORTANTE: Asegurate de que PostgreSQL este corriendo
echo            (Abrir pgAdmin 4 y verificar)
echo.
echo [*] Levantando aplicacion...
echo.
echo ========================================
echo   Aplicacion corriendo en:
echo   http://localhost:8000
echo ========================================
echo.
echo Presiona Ctrl+C para detener
echo.

python src/main.py
