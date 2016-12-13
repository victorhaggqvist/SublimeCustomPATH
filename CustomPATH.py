import os
import sublime


def plugin_loaded():
    # Sublime's default path on linux is
    # /usr/local/sbin:/usr/local/bin:/usr/bin:/usr/lib/jvm/default/bin:/usr/bin/site_perl:/usr/bin/vendor_perl:/usr/bin/core_perl
    settings = sublime.load_settings('CustomPATH.sublime-settings')

    path = settings.get('PATH')
    if len(path) > 0:
        if path not in os.environ['PATH']: # avoid inserting path multiple times
            override = settings.get('override', False)
            if override:
                os.environ['PATH'] = path
            else:
                append_front = settings.get('append_front')
                if append_front:
                    os.environ['PATH'] = path + os.pathsep + os.environ['PATH']
                else:
                    os.environ['PATH'] += os.pathsep + path
            print('Path loaded: %s' % os.environ['PATH'])
        else:
            print('Path loaded: %s' % os.environ['PATH'])
