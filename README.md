# What's this?
This repository is a nillerusr's Source Engine `dedicated` branch published to let users build and run dedicated servers

# How to Build?
Clone repo and change directory:
```
git clone https://github.com/AruMoon/source-engine-dedicated.git --recursive --depth 1
cd source-engine-dedicated
```
## On Linux:

Install dependencies:
fontconfig, freetype2, OpenAL, SDL2, libbz2, libcurl, libjpeg, libpng, zlib, libedit, libegl

### Supported servers
| Game | modname |
| --- | --- |
| Half-Life 2: Deathmatch | hl2mp |
| Day of Defeat: Source | dod |
### Source SDK 2013 supported servers
Change branch to ssdk-2013 to apply this
```
git checkout ssdk-2013
```
| Game | modname |
| --- | --- |
| Counter-Strike: Source | cstrike |

## Build:
`modname` should be from the tables above
```
./waf configure -T debug --build-game=modname --prefix=/path/to/game -d
./waf install
```

Prefix paramter should point to the root folder of the game. `/home/user/Half-Life 2` for example

Before executing install, delete all files in `bin` and `modname/bin` folders in game folder


## On Windows/MacOS:
**TODO(WAF is not configured for Windows/MacOS. Use VPC as temporary solution)**
