@echo off
IF "%~1"=="" (
    echo Error: Missing bug name
    exit /b 1
)

IF NOT EXIST ".\%~1\" (
    echo Error: Invalid bug name
    exit /b 1
)

py .\repair_python.py --project_path .\%~1 --mode line --epoch 20 --iter 200
py .\repair_python.py --project_path .\%~1 --mode tree --epoch 20 --iter 200
py .\result.py --project_path .\%~1 > .\%~1\results.txt
py .\apply_diffs.py --project_path .\%~1