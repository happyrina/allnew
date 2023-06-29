#!/bin/bash

input="user.dat"

while IFS=',' read -r username uid gid comment
do
	userdel -r $username$i
	echo "Delete $username"
done < $input
