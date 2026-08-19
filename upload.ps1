Set-Location "C:\Users\startklar\Python\Mein Projekt"

git add .

$message = Read-Host "Commit-Nachricht"
git commit -m $message

git push origin main

Read-Host "Fertig - Enter zum Schliessen"