Sash
====

Sugar Activity to display Open Badges on the XO that students have earned from playing various games.

For Developers
====

If you are interested in contributing to Sash, we recommend developing on a machine with a Linux OS. This will make it simple to install the necessary resources.

Open a command prompt and run:

    yum install sugar
    yum install sugar-emulator

Navigate to where you want to put the Sash repo

    git clone https://github.com/FOSSRIT/Sash.git -b develop

Navigate into the Sash repository

    python setup.py 

This will generate a .xo file that can be installed onto an XO or onto the sugar emulator

    sugar-install-bundle "sash.xo filename here"

This installs Sash into the sugar emulator

    sugar-emulator 

This will open the emulator and from there you can open the Sash activity to test it



Putting Sash support in your game
====

A couple activities that currently support Open Badges are:

    SkyTime
    Lemonade Stand

If you're interested in adding badge functionality to your game or activity, you will need to import the library found here https://github.com/FOSSRIT/sugar-badges
