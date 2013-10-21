#!/bin/bash

# Check if an external device exists
if [ -e /run/media/$USER/* ]; then

    # Build the .xo file
    ./setup.py dist_xo
    file=dist/*.xo

    # Check if the file already exists
    if [ -e /run/media/$USER/*/$file ]; then
        rm /run/media/$USER/*/$file
    fi

    # Move the new file onto the external device
    mv $file /run/media/$USER/*/
    rm -rf dist/

    # Notify the user a device was not found
    else
        echo 'No external device found.'
fi
