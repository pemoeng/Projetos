@echo off
git config --global user.email "pemo.eng@gmail.com"
git config --global user.name "pemoeng"
cd /d "%~dp0"
echo Rodando o script Python...
python atualizar_index.py

echo Subindo para o GitHub...
git add .
git commit -m "Atualizacao automatica"
git push --set-upstream origin main

echo.
echo Pronto! Site atualizado com sucesso!
pause