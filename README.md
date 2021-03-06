[![pipeline status](https://gitlab.com/AruMoon/source-engine-dedicated/badges/ssdk-2013/pipeline.svg)](https://gitlab.com/AruMoon/source-engine-dedicated/-/jobs)

# What's this?
This repository is a nillerusr's Source Engine `dedicated` branch published to let users build and run dedicated servers

# How to Build?
Clone repo and change directory:
```
git clone https://github.com/AruMoon/source-engine-dedicated.git --recursive
cd source-engine-dedicated
```
## On Linux:

Install dependencies:
zlib, libedit

You also need 32 bit versions of these libraries

On Debian/Ubuntu:
```
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install libedit-dev:i386 zlib1g-dev:i386 libedit-dev zlib1g-dev
```

### Supported servers for master branch
| Game | modname |
| --- | --- |
| Half-Life 2: Deathmatch | hl2mp |
| Day of Defeat: Source | dod |
### Supported servers for ssdk-2013 branch
Change branch to ssdk-2013 to apply this
```
git checkout ssdk-2013
```
| Game | modname |
| --- | --- |
| Counter-Strike: Source | cstrike |

## Build:
`modname` in command should be one from the tables above
```
./waf configure -T debug --build-game=modname --prefix=/path/to/game -d
./waf install
```

Prefix paramter should point to the root folder of the game. `/home/user/Counter-Strike Source Dedicated Server` for example

Before executing install, delete all files in `bin` and `modname/bin` folders in game folder


## On Windows/MacOS:
**TODO(WAF is not configured for Windows/MacOS. Use VPC as temporary solution)**
