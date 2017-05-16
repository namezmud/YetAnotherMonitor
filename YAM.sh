#! /bin/sh
### BEGIN INIT INFO
# Provides:          YAM
# Required-Start:    $all
# Required-Stop:
# Should-Start:      
# Default-Start:     
# Default-Stop:
# Short-Description: Run YetAnotherMonitor
# Description:       Run YetAnotherMonitor on startup
### END INIT INFO

PATH=/sbin:/bin:/usr/bin:/usr/local/sbin/

PROFILE=/var/run/YAM.pid

. /lib/init/vars.sh
. /lib/lsb/init-functions

NAME=YAM
RUN_AS=yam
CMD=/usr/local/sbin/YAM/YAMprocess_sensors.py
DIR=/usr/local/sbin/YAM/

do_start () {
	log_action_msg "start-stop-daemon --start --background --user $RUN_AS --pidfile $PIDFILE --chuid $RUN_AS --chdir=$DIR $CMD"
	start-stop-daemon --background --user $RUN_AS --pidfile $PROFILE --chuid $RUN_AS --chdir=$DIR --start $CMD --exec $CMD
}

do_stop() {
	start-stop-daemon --stop --user $RUN_AS
}

case "$1" in
  start|"")
	log_action_msg "Starting $NAME"
	do_start
	;;
  restart|reload|force-reload)
	log_action_msg "Restarting $NAME"
	do_stop
	do_start
	;;
  stop)
	log_action_msg "Stopping $NAME"
	do_stop
	;;
  status)
	;;
  *)
	echo "Usage: YAM.sh [start|stop|restart]" >&2
	exit 3
	;;
esac

exit 0
