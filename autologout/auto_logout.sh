#!/bin/bash

DELAY=2
TTY_TO=60


declare -a USER
declare -a TTY
declare -a GROUP
declare -a IDLE

init_data() {
    local i=0
    for index in `w -h|awk '{print $1";"$2}'`;do
        if [ ! -c /dev/${index#*;} ];then
            continue
        fi

        USER[$i]="${index%;*}"
        TTY[$i]="/dev/${index#*;}"
        IDLE[$i]=$(get_idle_seconds ${TTY[$i]})
        i=$(($i+1))
    done

    if [ $i -eq 0 ];then
        exit 0
    fi
}

get_idle_seconds() {
    current_sec=`date +%s`
    log_sec=`stat --format=%X "$1"`
    echo $((${current_sec}-${log_sec}))
}

send_msg() {
    local msg
    msg="${USER[$1]}: You ve been idle for ${IDLE[$1]} sec, allowed ${TTY_TO} sec\nYou need send a key"
    echo -e ${msg} | write ${USER[$1]} ${TTY[$1]}
}

kill_tty() {
    sleep ${DELAY}
    local idle_sec
    idle_sec=$(get_idle_seconds ${TTY[$1]})
    if [ ${TTY_TO} -ge ${idle_sec} ];then
          exit 0
    fi
    local pid_info
    pids=$(ps -eo pid,tty|grep ${TTY[$1]#/dev/}|awk '{print $1}'|tr '\n' ' ')
    kill -HUP $pids &> /dev/null
    sleep ${DELAY}
    for pid in $pids;do
        if kill -0 $pid &> /dev/null;then
            kill -TERM $pid
        fi
        sleep 2
        if kill -0 $pid &> /dev/null;then
            kill -KILL $pid
        fi
    done
}

check_idle() {
    local index=0
    for user in ${USER[@]};do
        if [ ${TTY_TO} -ge ${IDLE[$index]} ];then
            index=$(($index+1))
            continue
        fi

        send_msg $index
        kill_tty $index &
        index=$(($index+1))
    done
}

init_data
check_idle