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
> It is recommended to use Python Virtual Environment for development
### Install Prerequisites (Ubuntu)
```shell
sudo apt install python3-pyside2.qtwebenginewidgets git
sudo apt install -y --no-install-recommends python3-pip
```

### Get Source Code & Install required python packages
```shell
git clone https://gitlab.com/webyfy/iot/e-gurukul/yttv.git
cd yttv
pip3 install -r requirements.txt
```

### Run from Source
```shell
python3 -m yttv
```

### Debian Packaging
```shell
# Only for Ubuntu below 22.04(jammy)
sudo apt install -y software-properties-common && sudo add-apt-repository ppa:jyrki-pulliainen/dh-virtualenv -y

sudo apt install -y dh-virtualenv dpkg-dev debhelper make
pip3 install -U argparse-manpage
make deb
```

### AppImage
```shell
sudo apt install -y make binutils wget
pip3 install pyinstaller
make appimage
```
