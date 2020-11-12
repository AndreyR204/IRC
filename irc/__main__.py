#!/usr/bin/env python3
import argparse
from configparser import ConfigParser
import os
from irc import errors
from irc import client
import irc.const as const


def get_config() -> ConfigParser:
    current_config = ConfigParser()
    if not os.path.exists(const.CONFIG_PATH):
        raise errors.ConfigNotFoundError(os.getcwd())

    current_config.read(const.CONFIG_PATH)
    if not current_config.has_section("Settings") or not current_config.has_section("Servers"):
        raise errors.InvalidConfigError(current_config)

    return current_config


def refresh_config() -> None:
    config["Settings"]["nickname"] = client.username
    config["Settings"]["codepage"] = client.code
    for server in client.favourites:
        config.set("Servers", server)

    with open(const.CONFIG_PATH, "w") as file:
        config.write(file)


if __name__ == "__main__":
    try:
        config = get_config()
        client = client.Client(config["Settings"]["nickname"],
                               config["Settings"]["codepage"],
                               set(config["Servers"].keys()))
        client.start_client()
        refresh_config()
    except errors.ApiError as e:
        print(f"Client exception caught - {str(e)}")
    finally:
        exit()
