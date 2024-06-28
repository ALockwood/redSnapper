# redSnapper
A rapid screenshot utility using [BetterCam](https://github.com/RootKit-Org/BetterCam) to speed up my generation screenshots to be used in [YOLO](https://www.ultralytics.com/yolo) training data sets

## Why?
I needed something to quickly capture what was going on at variable frame rates and also wanted to play around with Python a bit more.

### No, Why "Red Snapper"?!
Well, it went something like this...
* I need something to take rapid screenshots at variable rates
* Screenshots are sort of snapshots
* I really only want what's in a specific _box_ on the screen
* Snapshots -> snap... what's in the box...
* ...[UHF](https://www.youtube.com/watch?v=KezvwARhBIc)...

LESSON: I should never be in charge of naming things 🙃

### Setup
1. If not already done, create a virtual env: `python -m venv .venv` 
1. Activate venv: (Win) `.venv\Scripts\activate`
1. Install requirements: `pip install -r requirements.txt`

## Running
On Windows run: `python redSnapper.py` then use the hotkeys to start/stop/exit

![example image](./docs/example.png)

### TODOs
1. Add a simple config file loader, probably leverage a `config.default` and then if `config.ini` exists, use that instead (add `config.ini` to `.gitignore`)
1. Once config is added, make directory, file prefix, hot keys, frame rate, detection area all configurable


