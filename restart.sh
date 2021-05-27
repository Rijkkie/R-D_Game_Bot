pkill -f main
git pull
set -e
nohup python3 main.py > console.log 2>&1 &