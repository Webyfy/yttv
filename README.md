# YouTube on TV
YouTube for 10 foot UI with D-pad navigation. It is a Site Specific Browser that points to https://www.youtube.com/tv with custom user-agent to avoid redirection.

## Installation

## Run from Source
Install prerequisites (Ubuntu)
```shell
sudo apt install python3-pyside2.qtwebenginewidgets

# Only for Ubuntu below 22.04(jammy)
sudo apt install -y software-properties-common && sudo add-apt-repository ppa:jyrki-pulliainen/dh-virtualenv -y

sudo apt install -y --no-install-recommends python3-pip
pip3 install -U pyinstaller argparse-manpage
```

Clone & Run
```shell
git clone https://gitlab.com/webyfy/iot/e-gurukul/yttv.git
cd yttv
python3 -m yttv
```
