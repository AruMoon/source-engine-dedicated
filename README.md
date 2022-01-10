# How to Build dedicated server?
Clone repo and change directory:
```
git clone https://github.com/AruMoon/source-engine --recursive --depth 1
cd source-engine
```
On Linux:

dependencies:
fontconfig, freetype2, OpenAL, SDL2, libbz2, libcurl, libjpeg, libpng, zlib
```
./waf configure -T debug -d
./waf build
```
On Windows/MacOS:
**TODO(WAF is not configured for Windows/MacOS. Use VPC as temporary solution)**
