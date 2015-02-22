# -*- coding: utf-8 -*-
# needs irclib v. 11.0.1
# scrape.py needs lxml and requests
# tested with python 3.4

from irc import client
from time import sleep
from sys import exit
import scrape

CHANNELS = ("#8/a/", "#/jp/radio")

def nm_to_nick(mask):
    """Converts nickmask to nick"""

    nm = client.NickMask(mask)
    return nm.nick

def on_ctcp(connection, event):

    print('received CTCP:', event.arguments[0])
    nick = nm_to_nick(event.source)
    if 'VERSION' in event.arguments:
        connection.ctcp_reply(nick, "VERSION Crappy bot by makos")
        print('CTCP reply to', event.source)
    elif 'PING' in event.arguments:
        connection.ctcp('PONG', nick)
        print('PONG sent to', event.source)

def on_priv(connection, event):

    print('received privmsg:', event.source, event.arguments)
    nick = nm_to_nick(event.source)
    if 'help' in event.arguments:
        connection.privmsg(nick, ".np - chiru.no now playing")
        connection.privmsg(nick, ".stats - chiru.no stats")
        connection.privmsg(nick, ".next  - chiru.no upcoming song")
    else:
        connection.privmsg(nick, "use 'help'")

def on_pub(connection, event):

    # print('pubmsg:', event.target)
    if '.np' in event.arguments:
        connection.privmsg(event.target, "chiru.no now playing: " + scrape.now_playing())
    elif '.stats' in event.arguments:
        stats = scrape.stats()
        connection.privmsg(event.target, "chiru.no stats:")
        for stat in stats:
            connection.privmsg(event.target, stat)
    elif '.next' in event.arguments:
        connection.privmsg(event.target, "chiru.no upcoming song: " + scrape.upcoming())

def on_invite(connection, event):

    print('received INVITE to', event.arguments[0], 'from', event.source)
    connection.join(event.arguments[0])

def on_quit(connection, event):

    print('connection dropped (?), reconnecting')
    connection.reconnect()

def main(address='irc.rizon.net', port=6667, nick='bwaka'):

    bot = client.Reactor()
    bot.add_global_handler("ctcp", on_ctcp)
    bot.add_global_handler("privmsg", on_priv)
    bot.add_global_handler("pubmsg", on_pub)
    bot.add_global_handler("invite", on_invite)
    bot.add_global_handler("quit", on_quit)

    server = bot.server()
    print('connecting...')
    server.connect(address, port, nick, username='bot', ircname='bot')
    
    if server.is_connected():
        print('connected')
        sleep(1)
        for channel in CHANNELS:
            server.join(channel)
        
        try:
            bot.process_forever()
        except KeyboardInterrupt:
            server.disconnect("bai")
            exit()
main()