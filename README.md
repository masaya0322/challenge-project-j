sudo git clone https://github.com/masaya0322/challenge-project-j.git /home/aj/game-iot

cd /home/aj/game-iot

sudo chmod +x /home/aj/game-iot/raspberry-pi/install.sh
sudo chmod +x /home/aj/game-iot/raspberry-pi/start_game.sh

./raspberry-pi/install.sh

sudo chown -R aj:aj /home/aj/game-iot
sudo chmod -R u+w /home/aj/game-iot


sudo reboot

ブランチ名：(feature,add,fix,refactor)/#ISSUE番号/ISSUEタイトル
英語で統一すること
