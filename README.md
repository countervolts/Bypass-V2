# what is this
complete rewrite and to be improved bypasser from my first version

# improved/new features

## new features
some new features include the FauxDisconnect added to this, within the old code it can be found [here](https://github.com/countervolts/Google-Wifi-Router-Bypasser/blob/94df52e0d5f4bb45945c6606602ff0cd7156016c/beta_features/features.py#L7)
- later on in development for the first bypasser I discovered a a hard bypass and simply ported it to this (note that this is just FauxDisconnect but improved), the source code to it can be found [here](https://github.com/countervolts/Google-Wifi-Router-Bypasser/blob/main/hard-bypass.py)

added a new mac address saver see the code [here](https://github.com/countervolts/Bypass-V2/blob/692e0c1d0934e8680d52274c6b0e26891b9ebbea/network/net.py#L83)

## improved
- improved exection speed by removing unnecessary functions and calls

removed the following
- checking if user is offline/online
- checking if user is using ethernet or wifi
- checking firewall for connections
- checking if bypass has been ran already
- removed all beta features entirely (except for FauxDisconnect)
- removed user debugging
- auto updater

as well improved bypassing feature which doesnt require the user to restart their computer
# how to run
either just run and download [main.exe](https://github.com/countervolts/Bypass-V2/releases/tag/released)

or you can run it using python

# how to run using python
1. first download [python](https://python.org/)
2. download the zip of this repo by clicking [this](https://github.com/countervolts/Bypass-V2/archive/refs/heads/main.zip)
3. extract it to desktop
4. after extracting, open command prompt and navigate to the directory by running:
    ```sh
    cd desktop/bypass-2
    ```
5. to install the needed packages/modules, run:
    ```sh
    pip install -r requirements.txt
    ```
6. after all the needed modules are installed, run:
    ```sh
    python main.py
    ```
7. it should all work properly
