#!/usr/bin/env python3
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
    if not current_config.has_section("Settings") \
            or not current_config.has_section("Servers"):
        raise errors.InvalidConfigError(current_config)

    return current_config


def refresh_config(client1) -> None:
    config1 = get_config()
    config1["Settings"]["nickname"] = client1.nickname
    config1["Settings"]["codepage"] = client1.code_page
    for server in client1.favourites:
        config1.set("Servers", server)

    with open(const.CONFIG_PATH, "w") as file:
        config1.write(file)


if __name__ == "__main__":
    try:
        config = get_config()
        client2 = client.Client(config["Settings"]["nickname"],
                               config["Settings"]["codepage"],
                               set(config["Servers"].keys()))
        client2.start_client()
        refresh_config(client2)
    except errors.ApiError as e:
        print(f"Client exception caught - {str(e)}")
    finally:
        exit()
