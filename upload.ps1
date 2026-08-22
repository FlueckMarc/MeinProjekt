Set-Location $PSScriptRoot

git add .
git commit -m "Update"
git push origin main

streamlit run app.py