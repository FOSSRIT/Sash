Sash
====

Sugar Activity to display Open Badges on the XO that students have earned from playing various games.

For Developers
====

If you are interested in contributing to Sash, we recommend developing on a machine with a Linux OS that has Python. This will make it simple to install the necessary resources and run Sash.

Open a command prompt and run:

    yum install sugar
    yum install sugar-emulator

Navigate to where you want to put the Sash repo and clone the repo

    git clone https://github.com/FOSSRIT/Sash.git -b develop

Navigate into the Sash repository and run the setup script
    
    cd Sash
    python setup.py 

This will generate a .xo file that can be installed onto an XO or onto the sugar emulator

    sugar-install-bundle "sash.xo filename here"

You can run the emulator by running the command

    sugar-emulator 

From there you can open the Sash activity to test it



Supporting Sash in your game
====

A couple activities that currently support Open Badges are:

    SkyTime
    Lemonade Stand

If you're interested in adding badge functionality to your game or activity, you will need to import the library found here https://github.com/FOSSRIT/sugar-badges
