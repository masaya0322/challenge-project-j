sudo git clone https://github.com/masaya0322/challenge-project-j.git /home/aj/game-iot

cd /home/aj/game-iot

sudo chmod +x raspberry-pi/install.sh

./raspberry-pi/install.sh

sudo chown -R aj:aj /home/aj/game-iot
sudo chmod -R u+w /home/aj/game-iot

sudo reboot