#!/bin/bash


if [ ! $UID -eq 0 ]
then
    echo "Need root permission"
    exit 1
fi

echo "uninstall convertd service"
service convertd stop 2> /dev/null
sleep 2
for pid in $(ps aux|grep -v grep|grep "convertd.py start"|awk -F ' ' '{print $2}');do
    kill -9 $pid
done
for pid in $(ps aux|grep -v grep|grep "convertd"|awk -F ' ' '{print $2}');do
    kill -9 $pid
done
chkconfig --del convertd 2> /dev/null
#/bin/rm /etc/init.d/convertdaemon 2> /dev/null
/bin/rm /etc/init.d/convertd 2> /dev/null

echo "clean auto start from /etc/rc.d/rc.local"
cat /etc/rc.d/rc.local |grep -v convertdaemon > /tmp/__ctmp_rclocal &&
/bin/mv /tmp/__ctmp_rclocal /etc/rc.d/rc.local
chmod 755 /etc/rc.d/rc.local

echo "remove files"
/bin/rm -r /usr/local/transcodec 2> /dev/null

