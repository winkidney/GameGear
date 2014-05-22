#---------------
#!/bin/sh

if [ $# != 1 ]
then 
    echo 'Usage: ctrl.sh start|stop|restart '
elif [ $1 = "start" ]
then
    python manage.py runfcgi method=threaded host=127.0.0.1 port=8050 maxchildren=300 pidfile=/tmp/gamegearfcgi.pid
elif [ $1 = "stop" ] 
then 
    kill `cat /tmp/gamegearfcgi.pid`
    echo 'process killed'
elif [ $1 = "restart" ]
then 
    kill `cat /tmp/gamegearfcgi.pid`
    echo 'process killed\n'
    python manage.py runfcgi method=threaded host=127.0.0.1 port=8050 maxchildren=300 pidfile=/tmp/gamegearfcgi.pid
    echo 'process started!'
fi
