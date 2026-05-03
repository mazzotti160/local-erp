@echo off
chcp 65001 > nul
echo Gerando LK ERP.exe...
pyinstaller lk_erp.spec --noconfirm --clean
echo.
if exist "dist\LK ERP.exe" (
    echo [OK] Executavel gerado com sucesso!
    echo Caminho: %~dp0dist\LK ERP.exe
) else (
    echo [ERRO] Falha ao gerar o executavel.
)
pause
