#!/bin/bash
if systemctl stop cm_chat.service ; then
    sudo cp /home/ubuntu/cm_chat/cm_chat.service /etc/systemd/system/
    sudo cp /home/ubuntu/cm_chat/dist/cm_chat /home/ubuntu/cm_chat
else
    echo "No all_telegram_bots.service found in system, now creating"
    sudo cp /home/ubuntu/cm_chat/cm_chat.service /etc/systemd/system
    sudo cp /home/ubuntu/cm_chat/dist/cm_chat /home/ubuntu/cm_chat
fi
sudo systemctl daemon-reload
sudo systemctl enable cm_chat.service
sudo systemctl start cm_chat.service
rm  /home/ubuntu/cm_chat.tar
