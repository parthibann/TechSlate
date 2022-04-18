#!/bin/bash

echo "techslate gid=$GID"
groupadd -g $GID techslate
usermod -a -G techslate techslate
if [ -z $USERPWD ]
then
  echo "User default password in use"
else
  echo "Changing user password"
  echo $USERPWD | passwd techslate --stdin
fi
# Starting shellinabox without password for techslate user
shellinaboxd --no-beep -t --user-css Normal:+/usr/share/shellinabox/black-on-white.css,Reverse:-/usr/share/shellinabox/white-on-black.css --service "/:techslate:techslate:/home/techslate:/bin/bash"

# This will request the user for password to login.
#shellinaboxd --no-beep -t -s "/:LOGIN"

