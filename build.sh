#!/bin/bash

# Check if an external device exists
if [ -e /run/media/$USER/* ]; then

    # Build the .xo file
    echo 'Found external device.'
    echo 'Building xo file...'
    ./setup.py dist_xo
    file=dist/*.xo

    # Check if the file already exists
    if [ -e /run/media/$USER/*/$file ]; then
        echo 'Removing version on device...'
        rm /run/media/$USER/*/$file
    fi 

    # Move the new file onto the external device
    echo 'Moving xo file to device...'
    mv $file /run/media/$USER/*/
    echo 'Cleaning up...'
    rm -r dist/

    # Notify the user a device was not found
    else
        echo 'No external device found.'
        echo 'Building xo file...'
        ./setup.py dist_xo
        mv dist/* ./
        echo 'Cleaning up...'
        rm -r dist/

    echo 'Finished!'
fi
