import argparse
import os
import sys
import time
import tomllib

from pynput.keyboard import Controller, KeyCode

CONFIG_PATH = "config.toml"


def get_resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def run(profile: str):
    shortcut: str = config.get(profile, {}).get("shortcut")
    if not shortcut:
        raise Exception("Profile not found")
    keyboard = Controller()
    key_combinations = shortcut.split(">")
    for combination in key_combinations:
        if combination.startswith("{") and combination.endswith("}"):
            action = combination.strip("{}").split(":")
            if action[0].lower() == "sleep":
                time.sleep(float(action[1]))
                continue
            if action[0].lower() == "press":
                if action[1].find("+") != -1:
                    keys = action[1].split("+")
                    for key in keys:
                        keyboard.press(KeyCode.from_vk(int(key)))
                else:
                    keyboard.press(KeyCode.from_vk(int(action[1])))
                continue
            if action[0].lower() == "release":
                if action[1].find("+") != -1:
                    keys = action[1].split("+")
                    for key in keys:
                        keyboard.release(KeyCode.from_vk(int(key)))
                else:
                    keyboard.release(KeyCode.from_vk(int(action[1])))
                continue
            if action[0].lower() == "tap":
                keyboard.tap(KeyCode.from_vk(int(action[1])))
                continue
            if action[0].lower() == "combine":
                keys = action[1].split("+")
                mapped_keys = [KeyCode.from_vk(int(key)) for key in keys]
                with keyboard.pressed(*mapped_keys):
                    pass
                continue


def argparser():
    parser = argparse.ArgumentParser(description="HotKeyStarter")
    parser.add_argument("-p", "--profile", help="Profile to use", required=True)
    parser.add_argument(
        "-c", "--config", help="Config to use", required=False, default=CONFIG_PATH
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = argparser()
    if args.config:
        CONFIG_PATH = args.config
    with open(get_resource_path(CONFIG_PATH), "rb") as config_file:
        config = tomllib.load(config_file)
    run(args.profile)
