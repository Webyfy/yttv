# YouTube on TV
YouTube for 10 foot UI with D-pad navigation. It is a Site Specific Browser that points to https://www.youtube.com/tv with custom user-agent to avoid redirection.

## Usage
```
usage: yttv [-h] [-d] [--version] [--freeze-on-focus-loss]

YouTube for 10 foot UI with D-pad navigation.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           start YouTube on TV in debug mode
  --version             show program's version number and exit
  --freeze-on-focus-loss
                        Freeze App on losing focus
```

## Development
### Prerequisites (Ubuntu)
```shell
sudo apt install python3-pyside2.qtwebenginewidgets
sudo apt install -y --no-install-recommends git python3-pip
```

### Run from Source
```shell
pip3 install -r requirements.txt
python3 -m yttv
```

### Debian Packaging
```shell
# Only for Ubuntu below 22.04(jammy)
sudo apt install -y software-properties-common && sudo add-apt-repository ppa:jyrki-pulliainen/dh-virtualenv -y

sudo apt install -y dh-virtualenv dpkg-dev debhelper make
pip3 install -r requirements.txt
pip3 install -U argparse-manpage
make deb
```

### AppImage
```shell
sudo apt install -y make binutils wget
pip3 install -r requirements.txt
pip3 install pyinstaller
make appimage
```
