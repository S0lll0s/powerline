#!/usr/bin/env python
# vim:fileencoding=utf-8:noet
from __future__ import (unicode_literals, division, absolute_import, print_function)

import os
import sys
import time

from threading import Lock, Timer
from argparse import ArgumentParser

from powerline.lemonbar import LemonbarPowerline


if __name__ == '__main__':
	parser = ArgumentParser(description='Powerline lemonbar bindings.')
	parser.add_argument(
		'--i3', action='store_true',
		help='Subscribe for i3 events.'
	)
	parser.add_argument(
		'--width', action='store', type=int,
		default=None, help='Maximum width the bar can occupy'
	)
	parser.add_argument(
		'theme', nargs='?', default='default',
		help='The theme to render')
	args = parser.parse_args()
	powerline = LemonbarPowerline(theme=args.theme)
	lock = Lock()
	modes = ["default"]
	write = get_unicode_writer(encoding='utf-8')

	def render(reschedule=False):
		if reschedule:
			Timer(0.5, render, kwargs={"reschedule": True}).start()

		global lock
		with lock:
			write(powerline.render(mode=modes[0], width=args.width))
			write('\n')
			sys.stdout.flush()

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
