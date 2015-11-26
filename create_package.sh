#!/bin/sh

# make sure the messages are up to date
git submodule update --init
./compile_msgs.sh

# get some extra meta-data, and append to the readme 
assisipy_rev=`git rev-parse HEAD`
assisi_msg_rev=`cd msg && git rev-parse HEAD`
assisipy_ver=`python -c "import assisipy; print assisipy.__version__"`

# but first, ensure we are working with the repo version
README=README.rst
#README=/dev/null
if [ -f "${README}" ] ; then
    git checkout -- ${README}
else
    echo "[I] skipping cleanup"
fi

printf "\n\n" | tee -a ${README}
printf "============================================================\n" | tee -a ${README}
printf "This release was sourced from:\n"               | tee -a ${README}
printf "\tassisi-python git rev %s\n" ${assisipy_rev}   | tee -a ${README}
printf "\tassisi-msg    git rev %s\n" ${assisi_msg_rev} | tee -a ${README}
printf "\tassisi-python version %s\n" ${assisipy_ver}   | tee -a ${README}
printf "============================================================\n" | tee -a ${README}

# exec the setup script to produce a package
python setup.py sdist
