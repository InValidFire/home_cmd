from argparse import ArgumentParser, Namespace
import asyncio
from lib.lights import LightHandler
from lib.tv.handler_tv import TVHandler


class HomeCMD:
    """Provides a CLI to control various smart objects in the house."""
    def __init__(self):
        parser = ArgumentParser("home_cmd", 
            description="control various smart home components from the command line.")
        subparsers = parser.add_subparsers()

        # lights subcommand setup
        lights_parser = subparsers.add_parser("lights", help="control the lights!")
        lights_parser.set_defaults(func=self.lights)
        lights_parser.add_argument("--light", "-l", help="target a specific light", default=None)
        lights_parser.add_argument("--find", "-f", action="store_true", 
            help="list all lights on the network.")
        lights_parser.add_argument("--brightness", "-b", default=None, help="set the light intensity")
        lights_parser.add_argument("--toggle", "-t", action="store_true", 
            help="toggle lights on/off")
        lights_parser.add_argument("--rename", 
            help="rename the light", default=None)
        lights_parser.add_argument("--scene", "-s", default=None, help="set the WiZ Scene")
        lights_parser.add_argument("--raw", "-r", action="store_true", help="toggle raw output", default=False)
        lights_parser.add_argument("--list", help="list lights or scenes", default=None)

        # tv subcommand setup
        tv_parser = subparsers.add_parser("tv", help="control the tv!")
        tv_parser.set_defaults(func=self.tv)
        tv_parser.add_argument("--find", "-f", action="store_true", 
            help="discover TVs on the network")
        tv_parser.add_argument("--tv", "-t", help="target a specific TV.", default=None)
        tv_parser.add_argument("--rename", help="rename the TV.", default=None)
        tv_parser.add_argument("--youtube", "-v", 
            help="play a YT video on the device.", default=None)
        tv_parser.add_argument("--list", "-l", help="list TVs or commands", default=None)
        tv_parser.add_argument("--mute", action="store_true", help="mute the tv(s).")

        args = parser.parse_args()

        args.func(args)

    def lights(self, args: Namespace):
        handler = LightHandler()
        event_loop = asyncio.new_event_loop()
        if args.find:
            print("Searching for lights...")
            lights = event_loop.run_until_complete(handler.discover_lights())
            if len(lights) == 0:
                print("No lights found on the network.")
        if isinstance(args.list, str) and args.list.lower() == "lights":
            lights = handler.get_lights()
            if not args.raw:
                print("Lights: ")
                for light in lights:
                    print("-", light.identifier)
            else:
                for light in lights:
                    print(light.identifier)
        elif isinstance(args.list, str) and args.list.lower() == "scenes":
            scenes = handler.get_scenes()
            if not args.raw:
                print("Scenes: ")
                for scene in scenes:
                    print("-", scene)
            else:
                for scene in scenes:
                    print(scene)

        if args.toggle and args.light is None:
            event_loop.run_until_complete(handler.toggle_all())
        elif args.toggle:
            event_loop.run_until_complete(handler.toggle(args.light))

        if args.rename is not None and args.light is not None:
            event_loop.run_until_complete(handler.rename(args.light, args.rename))
        elif args.rename is not None and args.light is None:
            print("Please specify the light you wish to rename")

        if args.scene is not None and args.light is not None:
            event_loop.run_until_complete(handler.set_scene(args.light, args.scene))
        elif args.scene is not None and args.light is None:
            event_loop.run_until_complete(handler.set_scene_all(args.scene))

        if args.brightness is not None and args.light is not None:
            event_loop.run_until_complete(handler.set_brightness(args.light, int(args.brightness)))
        elif args.brightness is not None and args.light is None:
            event_loop.run_until_complete(handler.set_brightness_all(int(args.brightness)))

    def tv(self, args: Namespace):
        handler = TVHandler()
        if args.find:
            print("Searching for TVs...")
            tvs = handler.discover_tvs()
            if len(tvs) == 0:
                print("No TVs found on the network.")

        if args.youtube and args.tv is not None:
            handler.play_youtube(args.tv, args.youtube)
        elif args.youtube:
            print("Please specify the TV you wish to play the video on.")

        if args.list == "commands" and args.tv is not None:
            commands = handler.get_commands(args.tv)
            print("Commands:")
            for command in commands:
                print("-", command)
        elif args.list == "commands" and args.tv is None:
            print("Please specify the TV you wish to get available commands for.")
        elif args.list is not None and args.list.lower() == "tvs":
            tvs = handler.get_tvs()
            print("TVs:")
            for tv in tvs:
                print("-", tv.identifier)

        if args.mute and args.tv is None:
            handler.toggle_mute_all()
        elif args.mute and args.tv is not None:
            handler.toggle_mute(args.tv)

        if args.rename is not None and args.tv is not None:
            handler.rename(args.tv, args.rename)
        elif args.rename is not None:
            print("Please specify the TV you wish to rename.")

HomeCMD()
