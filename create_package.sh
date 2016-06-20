#!/bin/sh

# make sure the messages are up to date
git submodule update --init
./compile_msgs.sh

# get some extra meta-data, and write to the VERSION file
assisipy_rev=`git rev-parse HEAD`
assisi_msg_rev=`cd msg && git rev-parse HEAD`
assisipy_ver=`python -c "import assisipy; print assisipy.__version__"`

# but first, ensure we are working with the repo version
VERSIONFILE=VERSION
#VERSIONFILE=/dev/null
if [ -f "${VERSIONFILE}" ] ; then
    git checkout -- ${VERSIONFILE}
else
    echo "[I] skipping cleanup"
fi

printf "\n" | tee ${VERSIONFILE}
printf "======================================================================\n" | tee -a ${VERSIONFILE}
printf "This release was sourced from:\n"               | tee -a ${VERSIONFILE}
printf "\tassisi-python git rev %s\n" ${assisipy_rev}   | tee -a ${VERSIONFILE}
printf "\tassisi-msg    git rev %s\n" ${assisi_msg_rev} | tee -a ${VERSIONFILE}
printf "\tassisi-python package version %s\n" ${assisipy_ver}   | tee -a ${VERSIONFILE}
printf "======================================================================\n" | tee -a ${VERSIONFILE}

# exec the setup script to produce a package
python setup.py sdist
