#!/bin/bash


start_caffeinate() {
    caffeinate &
    echo $! > /tmp/caffeinate.pid
}


stop_caffeinate() {
    if [ -f /tmp/caffeinate.pid ]; then
        kill $(cat /tmp/caffeinate.pid)
        rm /tmp/caffeinate.pid
    else
        echo "Caffeinate process not found"
    fi
}


if [ "$1" == "start" ]; then
    start_caffeinate
elif [ "$1" == "stop" ]; then
    stop_caffeinate
else
    echo "Usage: $0 {start|stop}"
fi