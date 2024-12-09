@echo off
echo Building the application...

:: 명령창 있는거
pyinstaller --onefile --name "ValidationSupportTool_xjera_console" --hidden-import=can.interfaces.vector --hidden-import=can.interfaces.kvaser --add-data "manual1_adb.png;." --add-data "autoreset.png;." --add-data "monkey.png;." --add-data "xjeraEasyTool.ico;." --icon=xjeraEasyTool.ico ValidationSupportTool_xjera.py


:: 생성된 실행 파일 폴더 열기
cd dist
start .

echo Build complete.
pause