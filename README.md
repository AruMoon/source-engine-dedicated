# What's this?
This repository is a nillerusr's Source Engine `dedicated` branch published to let users build and run dedicated servers or play on PC

# How to Build?
Clone repo and change directory:
```
git clone https://github.com/AruMoon/source-engine-dedicated.git --recursive --depth 1
cd source-engine-dedicated
```
### On Linux:

Dependencies:
fontconfig, freetype2, OpenAL, SDL2, libbz2, libcurl, libjpeg, libpng, zlib, libedit, libegl

Build game:
```
./waf configure -T debug --build-game=modname --prefix=/path/to/game
./waf install
```
Build dedicated server:
```
./waf configure -T debug --build-game=modname --prefix=/path/to/game -d
./waf install
```

On the `modname` you should place folder name of the mod. Mods are listed in this folder [https://github.com/AruMoon/source-engine-dedicated/tree/master/game/server](folder)

Prefix paramter should point to the root folder of the game. `/home/user/Half-Life 2` for example

Before executing install, delete all files in `bin` and `modname/bin` folders in game folder


### On Windows/MacOS:
**TODO(WAF is not configured for Windows/MacOS. Use VPC as temporary solution)**
