#!/bin/bash

CWD=$(pwd)
SWD=$(dirname $0)
ARGS=($@)

function __exit_trap() {
	cd "${CWD}" || exit 1
	if __in_conda_env; then
		conda deactivate || exit 1
		__exit_conda_env miniconda3-latest || exit $?
	fi
	if [ "$?" != "0" ]; then
		echo "Error occurred in $0 at line $1"
		exit $?
	else
		echo "Successfully executed $0"
	fi
}

trap '__exit_trap $LINENO' ERR EXIT

. "${SWD}/lib.sh" || exit $?

cd ${SWD}/../
__enter_conda_env miniconda3-latest || exit $?
conda activate ./.conda || exit $?

eval "$@" || exit $?

conda deactivate || exit $?
__exit_conda_env miniconda3-latest || exit $?