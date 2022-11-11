#!/bin/bash
if systemctl stop watcher.service ; then
    sudo cp /home/ubuntu/Watcher/services/watcher.service /etc/systemd/system/
    sudo cp /home/ubuntu/Watcher/dist/watcher /usr/bin/
else
    echo "No all_telegram_bots.service found in system, now creating"
    sudo cp /home/ubuntu/Watcher/services/watcher.service /etc/systemd/system
    sudo cp /home/ubuntu/Watcher/dist/watcher /usr/bin/
fi
sudo systemctl daemon-reload
sudo systemctl enable watcher.service
sudo systemctl start watcher.service
rm  /home/ubuntu/Watcher.tar
