@echo off
cd /d "G:\My Drive\Claude project\fibe\turley"

echo.
echo === Turley Energy — Deploy to Cloudflare ===
echo.

git add index.html about.html css/styles.css js/main.js images/

git diff --cached --quiet
if %errorlevel%==0 (
  echo No changes to deploy.
  echo.
  pause
  exit /b 0
)

set /p msg="Commit message (or press Enter for 'Update site'): "
if "%msg%"=="" set msg=Update site

git commit -m "%msg%"
git push origin master

echo.
echo Done! Cloudflare will deploy in ~30 seconds.
echo https://dash.cloudflare.com
echo.
pause
