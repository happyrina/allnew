#!/bin/bash
#
set -- $(getopt -q u:g:c:d:s:k:m "$@")
#
echo
while [ -n "$1" ]
do
	case "$1" in
	-u) param="$2"
	    echo "(uid) option, parameter value : $param"
	    shift ;;
	-g) param="$2"
	    echo "(gid) option, parameter value : $param"
	    shift ;;
	-c) param="$2"
	    echo "(comment) option, parameter value : $param"
	    shift ;;
	-d) param="$2"
	    echo "(home directory) option, parameter value : $param"
	    shift ;;
	-s) param="$2"
	    echo "(shell) option, parameter value : $param"
	    shift ;;
	-k) param="$2" 
	    echo "(initial scripts directory) option, parameter value : $param"
	    shift ;;
	-m) echo "(make home directory) option " ;;
	--) shift
	    break ;;
	*) echo "$1 is not an option" ;; 
	esac
	shift
done
#
count=1
for param in "$@"
do
	echo "Parameter #$count: $param"
	count=$[ $count + 1 ]
done
#
