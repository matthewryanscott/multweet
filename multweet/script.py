import sys

from pkg_resources import iter_entry_points

from multweet.config import Configuration, find_configuration_file
from multweet.logger import ERROR, INFO, log
from multweet.plugins import PLUGINS


def mtw():
    # Verify command line arg count.
    if len(sys.argv) < 2:
        log(ERROR, 'Must write a message on the command line.')
        sys.exit(1)
    # Read configuration.
    log(INFO, 'Reading configuration.')
    config = Configuration(find_configuration_file())
    # Read from stdin if desired; otherwise read from command line.
    if sys.argv[1] == '-':
        log(INFO, 'Reading message from stdin.  Use Ctrl+D when finished.')
        message = sys.stdin.read().strip()
    else:
        message = sys.argv[1:]
        message = ' '.join(message)
    # Split tag and message body.
    tag_name, body = message.split(None, 1)
    if tag_name.startswith('+'):
        tag_name = tag_name[1:]
        tag = config.tags[tag_name]
    else:
        tag = config.tags['DEFAULT']
        body = message
    # Make sure the tag posts to at least one account.
    log(INFO, 'Using %r', tag)
    if len(tag.accounts) == 0:
        log(ERROR, 'Tag does not post to any accounts.')
        sys.exit(1)
    # Verify message body length.
    log(INFO, 'Message body is %r', body)
    for account in tag.accounts:
        max_len = account.plugin.max_message_length
        if max_len is not None and len(body) > max_len:
            log(ERROR, 'Body must be %i or fewer characters.' % max_len)
            sys.exit(1)
    # Post message.
    for account in tag.accounts:
        log(INFO, 'Posting to %r', account)
        instance = account.plugin(account)
        instance.post_message(body)
    # Done.
    log(INFO, 'Message posted.')


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
