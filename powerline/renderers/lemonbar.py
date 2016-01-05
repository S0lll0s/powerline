# vim:fileencoding=utf-8:noet
from __future__ import (unicode_literals, division, absolute_import, print_function)

from powerline.renderer import Renderer
from powerline.colorscheme import ATTR_UNDERLINE


class LemonbarRenderer(Renderer):
	'''lemonbar (formerly bar/bar ain't recursive) renderer


	See documentation of `lemonbar <https://github.com/LemonBoy/bar>`_ and :ref:`the usage instructions <lemonbar-usage>`
	'''

	@staticmethod
	def hlstyle(*args, **kwargs):
		# We don’t need to explicitly reset attributes, so skip those calls
		return ''

	def hl(self, contents, fg=None, bg=None, attrs=None):
		text = ''

		if fg is not None:
			if fg is not False and fg[1] is not False:
				text += '%{{F#ff{0:06x}}}'.format(fg[1])
		if bg is not None:
			if bg is not False and bg[1] is not False:
				text += '%{{B#ff{0:06x}}}'.format(bg[1])

		if attrs & ATTR_UNDERLINE:
			text += '%{+u}'

		return text + contents + '%{F-B--u}'

	def render(self, output=None, *args, **kwargs):
		self.segment_info['output'] = output
		return '%{{l}}{0}%{{r}}{1}'.format(
			super(LemonbarRenderer, self).render(side='left', *args, **kwargs),
			super(LemonbarRenderer, self).render(side='right', *args, **kwargs),
		)


renderer = LemonbarRenderer
