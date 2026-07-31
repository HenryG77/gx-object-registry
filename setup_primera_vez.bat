@echo off
echo ========================================
echo   GeneXus Object Registry
echo   SETUP PRIMERA VEZ
echo ========================================
echo.

echo [1/3] Creando tablas en la base de datos...
echo        (Asegurate de que PostgreSQL este corriendo)
echo.
alembic upgrade head

echo.
echo [2/3] Cargando datos iniciales (tipos de objeto)...
python scripts/seed_database.py

echo.
echo [3/3] Setup completado!
echo.
echo ========================================
echo   LISTO PARA USAR
echo ========================================
echo.
echo Para iniciar la aplicacion, ejecuta:
echo   iniciar.bat
echo.
echo O manualmente:
echo   python src/main.py
echo.
pause
