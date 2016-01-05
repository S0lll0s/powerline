from __future__ import (unicode_literals, division, absolute_import, print_function)

import sys
import time
import re
import subprocess

from threading import Lock, Timer
from argparse import ArgumentParser

from powerline.lemonbar import LemonbarPowerline
from powerline.lib.monotonic import monotonic
from powerline.lib.dict import mergedicts


if __name__ == '__main__':
    parser = ArgumentParser(description='Powerline BAR bindings.')
    parser.add_argument(
        '--i3', action='store_true',
        help='Subscribe for i3 events.'
    )
    args = parser.parse_args()

    themes = {
        'LVDS1': 'default',
        'HDMI1': 'hdmi',
        'VGA1': 'hdmi'
    }

    active_screens = [
        dict(zip(['name', 'width', 'height', 'x', 'y'], values))
        for values in re.findall(
            '^(\w+) connected (\d+)x(\d+)\+(\d+)\+(\d+)',
            subprocess.check_output("xrandr -q", shell=True).decode(),
            re.MULTILINE
        )
    ]

    powerlines = []

    for screen in active_screens:
        theme_name = "default"
        if 'HDMI1' in screen['name']:
            theme_name = 'hdmi'
        elif 'DVI' in screen['name'] or 'VGA' in screen['name']:
            theme_name = 'dvi'

        line = LemonbarPowerline(theme=theme_name, output=screen['name'])
        process = subprocess.Popen("bar-aint-recursive -g {}x16+{} -f 'Source Code Pro for Powerline-9,Icon-9'".format(screen['width'], screen['x']), shell=True, stdin=subprocess.PIPE)
        powerlines.append((line, process, int(screen['width'])/5))


    lock = Lock()
    modes = ["default"]

    def render(reschedule=False):
        if reschedule:
            Timer(0.5, render, kwargs={"reschedule": True}).start()

        global lock
        with lock:
            for line, process, width in powerlines:
                process.stdin.write(line.render(mode=modes[0], width=width).encode("utf-8")+b'\n')

    def update(evt):
        modes[0] = evt.change
        render()

    render(reschedule=True)

    if args.i3:
        try:
            import i3ipc
        except ImportError:
            import i3
            i3.Subscription(lambda evt, data, sub: print(render()), 'workspace')
        else:
            conn = i3ipc.Connection()
            conn.on('workspace::focus', lambda conn, evt: render())
            conn.on('mode', lambda conn, evt: update(evt))
            conn.main()

    while True:
        time.sleep(1e8)
