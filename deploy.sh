#! /bin/bash

SSH_USERNAME="pi"
SSH_PWD="raspberry"
THIS_DIR="/home/xavier/Desktop/XAVI/PROJECTS/NetroZim/clayton"
FLASK_APP="$THIS_DIR/FLASK_APP"

for ITEM in $(ls $FLASK_APP)
	do
		if [ "$ITEM" == "venv" ]
		then
			continue
		else
			SCP_SOURCES="$SCP_SOURCES $FLASK_APP/$ITEM"
		fi

done

SCP_DEST="pi@192.168.0.121:/home/pi/clayton/FLASK_APP";

sshpass -p "$SSH_PWD" scp -r $SCP_SOURCES $SCP_DEST