from pkg_resources import iter_entry_points

from multweet.config import Configuration, find_configuration_file
from multweet.plugins import PLUGINS


def mtw():
    pass


def listplugins():
    print 'MulTweet plugins'
    print '================'
    print
    for name, plugin in sorted(PLUGINS.iteritems()):
        print '%s: %s' % (name, plugin.__doc__.strip())


def listaccounts():
    print 'MulTweet accounts'
    print '================='
    print
    config = Configuration(find_configuration_file())
    for account_name in sorted(config.accounts):
        account = config.accounts[account_name]
        print account


def listtags():
    print 'MulTweet tags'
    print '============='
    print
    config = Configuration(find_configuration_file())
    for tag_name in sorted(config.tags):
        tag = config.tags[tag_name]
        print tag
