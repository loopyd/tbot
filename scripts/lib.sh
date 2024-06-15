#!/bin/bash

if [ "${BASH_SOURCE[0]}" == "${0}" ]; then
	echo "This script must be sourced, not executed."
	exit 1
fi

# ==============================================================================
# Colors
# ==============================================================================

C_Reset="\033[0m"

# Normal                 Bold                       Underline
C_Black="\033[0;30m";    C_B_Black="\033[1;30m";    C_U_Black="\033[4;30m"  
C_Red="\033[0;31m";      C_B_Red="\033[1;31m";      C_U_Red="\033[4;31m"    
C_Green="\033[0;32m";    C_B_Green="\033[1;32m";    C_U_Green="\033[4;32m" 
C_Yellow="\033[0;33m";   C_B_Yellow="\033[1;33m";   C_U_Yellow="\033[4;33m"
C_Blue="\033[0;34m";     C_B_Blue="\033[1;34m";     C_U_Blue="\033[4;34m" 
C_Purple="\033[0;35m";   C_B_Purple="\033[1;35m";   C_U_Purple="\033[4;35m"
C_Cyan="\033[0;36m";     C_B_Cyan="\033[1;36m";     C_U_Cyan="\033[4;36m"
C_White="\033[0;37m";    C_B_White="\033[1;37m";    C_U_White="\033[4;37m" 

# High Intensty          Bold High Intensity        Underline High Intensity
C_I_Black="\033[0;90m";  C_I_B_Black="\033[1;90m";  C_I_U_Black="\033[4;90m"
C_I_Red="\033[0;91m";    C_I_B_Red="\033[1;91m";    C_I_U_Red="\033[4;91m"    
C_I_Green="\033[0;92m";  C_I_B_Green="\033[1;92m";  C_I_U_Green="\033[4;92m"
C_I_Yellow="\033[0;93m"; C_I_B_Yellow="\033[1;93m"; C_I_U_Yellow="\033[4;93m"
C_I_Blue="\033[0;94m";   C_I_B_Blue="\033[1;94m";   C_I_U_Blue="\033[4;94m"   
C_I_Purple="\033[0;95m"; C_I_B_Purple="\033[1;95m"; C_I_U_Purple="\033[4;95m"
C_I_Cyan="\033[0;96m";   C_I_B_Cyan="\033[1;96m";   C_I_U_Cyan="\033[4;96m"
C_I_White="\033[0;97m";  C_I_B_White="\033[1;97m";  C_I_U_White="\033[4;97m"

# Normal background     High Intensity Background
On_Black="\033[40m";    On_IBlack="\033[0;100m"
On_Red="\033[41m";      On_IRed="\033[0;101m"     
On_Green="\033[42m";    On_IGreen="\033[0;102m"
On_Yellow="\033[43m";   On_IYellow="\033[0;103m"
On_Blue="\033[44m";     On_IBlue="\033[0;104m"
On_Purple="\033[45m";   On_IPurple="\033[10;95m"
On_Cyan="\033[46m";     On_ICyan="\033[0;106m"
On_White="\033[47m";    On_IWhite="\033[0;107m"

function __check_cmd() {
	if ! command -v $1 &>/dev/null; then
		echo "$1 is not installed. Please install it first."
		return 1
	fi
	return 0
}

function __check_pyenv_version() {
	local _version=$1
	if ! pyenv versions | grep -q $_version; then
		return 1
	fi
	return 0
}

function __ensure_pyenv_version() {
	local _pyenv_name=$1
	__check_cmd pyenv || return $?
	__check_pyenv_version "${_pyenv_name}" || {
		pyenv install $_pyenv_name || {
			return 2
		}
	}
	pyenv local $_pyenv_name || {
		return 3
	}
	return 0
}

function __in_conda_env() {
	if [ -z "$CONDA_DEFAULT_ENV" ]; then
		return 1
	fi
	return 0
}

function __add_to_path() {
	local _path=$1
	if [[ ! "$PATH" =~ (^|:)"$_path"(:|$) ]]; then
		newpath="$_path:$PATH"
		export PATH="${newpath}"
	fi
}

function __remove_from_path() {
	local _path=$1
	newpath=$(echo $PATH | tr ':' '\n' | grep -v $_path | tr '\n' ':')
	export PATH="${newpath}"
}

function __enter_conda_env() {
	local _pyenv_name=$1
	__ensure_pyenv_version "$_pyenv_name" || return $?
	eval "$(conda shell.bash hook 2>/dev/null)" || return $?
	__add_to_path "$(pyenv prefix ${_pyenv_name})/bin" || return $?
	. $(pyenv prefix ${_pyenv_name})/etc/profile.d/conda.sh || return $?
}

function __exit_conda_env() {
	local _pyenv_name=$1
	__ensure_pyenv_version "$_pyenv_name" || return $?
	conda deactivate || return $?
	__remove_from_path "$(pyenv prefix ${_pyenv_name})/bin" || return $?
	pyenv local --unset || return $?
}

function __clean_items() {
	local _items=$@
}