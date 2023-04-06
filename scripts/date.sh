echo "установлен часовой пояс Москва"
sudo unlink /etc/localtime
sudo ln -s /usr/share/zoneinfo/Europe/Moscow /etc/localtime
date

echo "установка модулей для python"
pip install -r requirements.txt