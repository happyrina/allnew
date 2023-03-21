#!/bin/bash

opt=$1

if [ $opt == 'test' -a $opt == 'aaa' ]; then
	echo good
elif [ $opt == 'test' -o $opt == 'bbb' ]; then
	echo bad
else
	echo "Input two parameters...!!"
fi
	
