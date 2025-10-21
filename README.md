# DJ GAME CONTROLLER 
**DGC** will let you map your DJ controller console as a game controller.

## Dependencies
- [Git](https://git-scm.com/downloads) : for version control.
- [ViGEmBus Driver](https://vigembusdriver.com/download/) : For creating a virtuall xbox controller.

## Setup

### Install ViGEmBus Driver
link: [ViGEmBus Driver](https://vigembusdriver.com/download/)

Follow the on screen instrustions and restart you computer after install.

> NOTE: You should see see XBOX 360 Peripherals in your device manager

### Install Python 3.11
link: [Python 3.11.13](https://www.python.org/downloads/release/python-31113/)

While installing, make sure to **check the box: "Add Python to PATH".**
Since rtmidi is not supported by the newer versions, we need to install an older version of python.

### Clone the repository
```sh
git clone https://github.com/AyushSMD/DJ-Game-Controller.git
cd DJ-Game-Controller
```

### Create a virtual enviroment

```sh
py -3.11 -m venv DGCenv
DGCenv\Scripts\Activate.ps1
```
this will use python 3.11 as default.

### Install the required packages

```sh
pip install python-rtmidi vgamepad
```

## Configuration

