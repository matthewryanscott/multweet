import os

from configobj import ConfigObj

from multweet.plugins import PLUGINS


class Configuration(object):
    
    def __init__(self, filename):
        self.accounts = {}
        self.tags = {}
        self._load(filename)
    
    def _load(self, filename):
        config = ConfigObj(filename)
        # Parse accounts.
        for name in config.sections:
            if name.startswith('account:'):
                account_name = name[len('account:'):]
                options = dict(config[name])
                plugin_name = options.pop('plugin')
                plugin = PLUGINS[plugin_name]
                account = Account(account_name, plugin, options)
                self.accounts[account_name] = account
        # Parse tags.
        for name in config.sections:
            if name.startswith('tag:'):
                tag_name = name[len('tag:'):]
                options = config[name]
                include_spec = options.get('include', '').strip()
                exclude_spec = options.get('exclude', '').strip()
                accounts = set()
                # First handle includes.
                if include_spec == '*':
                    accounts = set(self.accounts.values())
                else:
                    for account_name in include_spec.split():
                        accounts.add(self.accounts[account_name])
                # Next handle excludes.
                if exclude_spec == '*':
                    accounts = set()
                else:
                    if include_spec == '':
                        accounts = set(self.accounts.values())
                    for account_name in exclude_spec.split():
                        accounts.remove(self.accounts[account_name])
                tag = Tag(tag_name, accounts)
                self.tags[tag_name] = tag


class Account(object):

    def __init__(self, name, plugin, options):
        self.name = name
        self.plugin = plugin
        self.options = options

    def __repr__(self):
        return '<Account name:%s plugin:%s>' % (self.name, self.plugin.name)


class Tag(object):
    
    def __init__(self, name, accounts):
        self.name = name
        self.accounts = accounts
    
    def __repr__(self):
        return '<Tag name:%s>' % (self.name)


def find_configuration_file():
    return os.path.abspath(
        os.path.join(
            os.environ['HOME'],
            '.multweetrc',
        )
    )
