# vim:fileencoding=utf-8:noet
from __future__ import (unicode_literals, division, absolute_import, print_function)

from powerline import Powerline
from powerline.lib.dict import mergedicts


class LemonbarPowerline(Powerline):
    def init(self, theme=None, output=None):
        super(LemonbarPowerline, self).init(ext='wm', renderer_module='lemonbar')
        self.config_override = {"ext": {"wm": {"theme": theme}}}
        self.output = output

    def render(self, *args, **kwargs):
        return super(LemonbarPowerline, self).render(output=self.output, *args, **kwargs)

    def load_main_config(self):
            r = super(LemonbarPowerline, self).load_main_config()
            if self.config_override:
                    mergedicts(r, self.config_override)
            return r
