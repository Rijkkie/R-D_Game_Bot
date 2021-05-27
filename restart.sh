pkill -f main
git pull git@github.com:Rijkkie/Game_Bot.git main
set -e
nohup python3 main.py > console.log 2>&1 &
