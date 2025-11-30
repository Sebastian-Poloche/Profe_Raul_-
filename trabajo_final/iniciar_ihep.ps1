Write-Host "IHEP - Sistema de Herramientas" -ForegroundColor Cyan


$venvPython = ".\.venv\Scripts\python.exe"
$workDir = Get-Location

if (-not (Test-Path $venvPython)) {
    Write-Host "ERROR: No se encuentra el entorno virtual" -ForegroundColor Red
    exit 1
}

Write-Host "[1/3] Detendiendo procesos anteriores..." -ForegroundColor Yellow
Get-Process python* -ErrorAction SilentlyContinue | ForEach-Object { 
    Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue 
}
Start-Sleep -Seconds 2

Write-Host "[2/3] Iniciando Backend Django..." -ForegroundColor Green
$backendJob = Start-Job -ScriptBlock {
    cd "c:\Users\chatarra\Documents\Profe_Raul_-\trabajo_final\backend"
    & "C:\Users\chatarra\Documents\Profe_Raul_-\trabajo_final\.venv\Scripts\python.exe" manage.py runserver 127.0.0.1:8000
}

Start-Sleep -Seconds 4

Write-Host "[3/3] Iniciando Frontend..." -ForegroundColor Green
$frontendJob = Start-Job -ScriptBlock {
    cd "c:\Users\chatarra\Documents\Profe_Raul_-\trabajo_final"
    & "C:\Users\chatarra\Documents\Profe_Raul_-\trabajo_final\.venv\Scripts\python.exe" main.py
}

Write-Host "Sistema IHEP iniciado" -ForegroundColor Green


Write-Host "Backend: http://127.0.0.1:8000" -ForegroundColor Yellow
Write-Host "API: http://127.0.0.1:8000/api/" -ForegroundColor Yellow
Write-Host "`nPresiona CTRL+C para detener el sistema`n" -ForegroundColor Cyan


while ($true) {
    Start-Sleep -Seconds 1
    
    if ((Get-Job -Id $backendJob.Id).State -ne "Running" -or 
        (Get-Job -Id $frontendJob.Id).State -ne "Running") {
        Write-Host " Sistema detenido" -ForegroundColor Yellow
        break
    }
}
