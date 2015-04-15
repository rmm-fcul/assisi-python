#!/bin/sh

ipA=194.117.20.244
ipB=127.0.0.1
saA=5455
paA=5456
saB=5755
paB=5756

# select the experiment configuration desired
# note: currently only cfg-sim
rtcpath=cfg-sim
# define the location to the assisi-python installation
assisipy_dir=/home/rmm/repos/gh/rmm-assisipy
# define the location of the assisi playground simulator binary
playground_dir=/home/rmm/projects/assisi/enki/playground-larics-head/build/playground

# use these flags (=0/1) to control which stages are executed.
st_sim=1
spawn=1
st_bee=1
prep_casu=1
st_casu=1
ECHO=


### ============== shouldn't need to bedit below this point ============== ###
### ============== ======================================== ============== ###
# what this script does
#
# 1. launch both instances of the simulator
# 2. spawn the objects
# 3. run bees behaviour (A only)
# 4. run CASU behaviour (A -- sensors)
# 5. run CASU behaviour (B -- aggregator)


arena=${1:-A} # make the sensor arena the default.

script_dir=${PWD} # this WON'T WORK IF THE script not exec locally!

# default choices (all env B)
other=sensors
this=monitor
my_pp=${paB}
my_sp=${saB}
my_ip=${ipB}
# switch if arg is opposite
if [ "${arena}" = "A" ] ; then
    this=sensors
    other=monitor
    my_pp=${paA}
    my_sp=${saA}
    my_ip=${ipA}
fi

# bit of a cludge having both $pp and $pa
my_pa="tcp://*:${my_pp}"
my_sa="tcp://*:${my_sp}"

if [ "${arena}" = "A" ] ; then
    echo "I'm doing sensors(${this})"
else
    echo "I'm doing monitoring(${this})"
fi

PIDS=""
# 0. setup python path
pcmd="export PYTHONPATH=${PYTHONPATH}:${assisipy_dir}:" 
echo "[I] (0) updating python path: \t${pcmd}"
${pcmd}


# 1. launch playground
if [ ${st_sim} -ne 0 ] ; then
    cd ${playground_dir}; echo "\tin" `pwd`
    cmd=" ./assisi_playground --pub_addr ${my_sa} --sub_addr ${my_pa}"
    echo "[I] (1) REVERSED PA/SA: bg executing ${cmd}"
    #cmd=" ./assisi_playground --pub_addr ${my_pa} --sub_addr ${my_sa}"
    #echo "[I] (1) executing ${cmd}"
    ${cmd} &
    playground_pid=$!
    PIDS=${PIDS}"$! "
    #PIDS+="$! "
fi

# 2. spawn the objects 
if [ ${spawn} -ne 0 ] ; then
    if [ "${arena}" = "A" ] ; then
        cmd="python spawn_monitor_arena.py -svr ${my_ip} -pp ${my_pp}"
    else
        cmd="python spawn_sensors_arena.py -svr ${my_ip} -pp ${my_pp}"
    fi
    cd ${script_dir}; echo "\tin" `pwd`
    echo "[I] (2) spawning objects: ${cmd}"
    ${cmd}
fi

# 3. run bees behaviour (A only)
if [ ${st_bee} -ne 0 ] ; then
    if [ "${arena}" = "A" ] ; then
        # faz nada...
        :
    else
        cd ${script_dir}; echo "\tin" `pwd`
        cmd="python bees_circling.py -svr ${my_ip} -pp ${my_pp} -sp ${my_sp}"
        echo "[I] (3) exec bee behaviour: ${cmd}"
        ${cmd} &
        #echo "[D] (3) bee shell PID is $! (dollar dollar is $$)"
        PIDS=${PIDS}"$! "

    fi
fi

# 4a. prep CASU rtc files.
if [ ${prep_casu} -ne 0 ] ; then
    cd ${script_dir}; echo "\tin" `pwd`
    # copy the template file
    tgtl=casu-sensor-left.rtc
    tgtr=casu-sensor-right.rtc
    tgtm=casu-monitor.rtc 

    for tgt in ${tgtl} ${tgtr} ${tgtm}; do
        ${ECHO} cp ${rtcpath}/template/${tgt} ${rtcpath}/${tgt}
        # do inline replace to setup host IPs
        
        ${ECHO} sed -i "s/@HOSTB@/${ipB}/g" ${rtcpath}/${tgt}
        ${ECHO} sed -i "s/@HOSTA@/${ipA}/g" ${rtcpath}/${tgt}
        ${ECHO} sed -i "s/@PUBADDRB@/${paB}/g" ${rtcpath}/${tgt}
        ${ECHO} sed -i "s/@SUBADDRB@/${saB}/g" ${rtcpath}/${tgt}
        ${ECHO} sed -i "s/@PUBADDRA@/${paA}/g" ${rtcpath}/${tgt}
        ${ECHO} sed -i "s/@SUBADDRA@/${saA}/g" ${rtcpath}/${tgt}
    done
    #sed -i.bak s/STRING_TO_REPLACE/STRING_TO_REPLACE_IT/g index.html
fi


# 4. run CASU behaviour 
if [ "${arena}" = "A" ] ; then
    # generate commands
    cd ${script_dir}; echo "\tin" `pwd`
    cmd3="python monitor.py --rtc-path ${rtcpath} --name casu-monitor" 
    if [ ${st_casu} -ne 0 ] ; then
        # in this branch exc,
        echo "[I] (5) exec CASUs in N arena (i): ${cmd3}"
        ${cmd3} &
        PIDS=${PIDS}"$! "
    else
        # this branch, just display them
        echo "[G] (4) command for CASUs N(iii):  ${cmd3}"

    fi

    # faz nada...
    :
else
    # generate commands
    cd ${script_dir}; echo "\tin" `pwd`
    cmd1="python spoke.py --rtc-path ${rtcpath} --name casu-sensor-left -d W"
    cmd2="python spoke.py --rtc-path ${rtcpath} --name casu-sensor-right -d W"
    if [ ${st_casu} -ne 0 ] ; then
        # in this branch exc,
        echo "[I] (4) exec CASUs in N arena (i): ${cmd1}"
        ${cmd1} &
        PIDS=${PIDS}"$! "
        echo "[I] (4) exec CASUs in N arena (ii): ${cmd2}"
        ${cmd2} &
        PIDS=${PIDS}"$! "
    else
        # this branch, just display them
        echo "[G] (4) command for CASUs N(i):  ${cmd1}"
        echo "[G] (4) command for CASUs N(ii): ${cmd2}"

    fi
fi


#st_casu=0
# 5. run CASU behaviour (B -- aggregator)


#print_pids=$(printf " %s" "${PIDS[@]}")
echo "\n\n\n"
echo "[I] bg process PIDs are ${PIDS}"
echo "[I] type: kill -15 ${PIDS}"

