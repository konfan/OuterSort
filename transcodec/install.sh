#!/bin/bash

INSTALLDIR=$PWD

detectrootpermission() {
    userID=$UID
    if [ ! $userID  -eq 0 ]
    then
        echo "Need root permission to install"
        exit 1
    fi
}
testmodule() {
    # test if python module $1
    # return 1 if installed, or return 0
    modulename=$1
    tmp=$(python -c "import $modulename" 2>&1)
    if test -z "$tmp"
    then
        return 1
    fi
    return 0
}

install_pidfile() {
    cd $INSTALLDIR &&
    modulename=lockfile
    echo "checking $modulename"
    testmodule "$modulename"
    if [ $? -eq 0 ]
    then
        filename=$(ls|grep $modulename.*tar) 
        if test ! -e "$filename" 
        then
            echo "can't open install file"
        fi
        tar -xf "$filename" &&
        cd $(ls |grep $modulename|grep -v tar) &&
        python setup.py install 
        cd $INSTALLDIR 
        testmodule "$modulename"
        if [ $? -eq 0 ]
        then
            echo "install failed, please install lockfile-0.9.1 manually"
            exit 1
        fi
    fi
    echo "done"
}

install_daemon() {
    cd $INSTALLDIR &&
    modulename="daemon"
    echo "checking $modulename"
    testmodule "$modulename"
    if [ $? -eq 0 ]
    then
        filename=$(ls|grep $modulename.*tar) 
        if test ! -e "$filename"
        then
            echo "can't open install file"
        fi
        tar -xf "$filename" &&
        cd $(ls |grep python.*$modulename|grep -v tar) &&
        python setup.py install 
        cd $INSTALLDIR 
        testmodule "$modulename"
        if [ $? -eq 0 ]
        then
            echo "install failed, please install python-daemon-1.5.5 manually"
            exit 1
        fi
    fi
    echo "done"
}

applypatch() {
    dst=$(python -c "import os,daemon;print(os.path.split(daemon.__file__)[0])")
    /bin/rm ${dst}/*.pyc
    dst=$dst"/pidlockfile.py"
    pfile=$INSTALLDIR"/daemon.patch"
    if  test ! -e "$dst" 
    then
        echo "can't open $dst"
        return 1
    fi

    if test ! -e "$pfile"
    then
        echo "can't open $pfile"
        return 1
    fi

    echo "patching $dst"
    patch -usN -r - "$dst" "$pfile" > /dev/null

    return 0
}

start_service() {
    #cat /etc/crontab |grep -v "convertd.py start" > /tmp/crontab$$
    #echo "* * * * * root python /usr/local/transcodec/service/convertd.py start >/dev/null 2>&1" >> /tmp/crontab$$
    #/bin/mv /tmp/crontab$$ /etc/crontab
    #service crond restart
	if test ! -e "/usr/local/transcodec/convertdaemon" > /dev/null 2>&1
	then
		echo "can't create daemon process, please reinstall"  
	fi
	/usr/local/transcodec/convertdaemon &
}

detectrootpermission
install_pidfile
install_daemon
applypatch
if [ ! $? -eq 0 ]
then
    echo "patch failed"
    exit 1
fi
/bin/cp -ar ${INSTALLDIR}/transcodec /usr/local/
/bin/cp -a ${INSTALLDIR}/transcodec/convertd /etc/init.d/
chmod a+x /etc/init.d/convertd
chkconfig --add convertd

#/bin/cp -a ${INSTALLDIR}/transcodec/convertdaemon /etc/init.d/
#chmod a+x /etc/init.d/convertdaemon
#chkconfig --add convertdaemon
chmod a+x /usr/local/transcodec/convertdaemon
cat /etc/rc.d/rc.local |grep -v convertdaemon > /tmp/__ctmp_rclocal &&
echo "/usr/local/transcodec/convertdaemon &" >> /tmp/__ctmp_rclocal &&
/bin/mv /tmp/__ctmp_rclocal /etc/rc.d/rc.local
chmod 755 /etc/rc.d/rc.local
start_service


