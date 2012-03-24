Youtuber
========

Youtuber allows you to create an Atom feed out of a Youtube channel, complete
with HD video enclosures allowing you to subscribe to the channel with the
podcast client of your choice, and view the downloaded videos with the player
of your choice.


Requirements
------------

You'll need:

- Python
- youtube-dl (http://rg3.github.com/youtube-dl/, or in Ubuntu:
  `sudo apt-get install youtube-dl`
- A webserver, like Apache (only if you don't want to host
  videos locally)
- Linux or Mac (if somebody can make this work on Windows, be my guest)

After downloading the source, build out the project (from the checkout
directory).  Bootstrapping may need to be run with "sudo", depending on
how you've installed Python::

    $ python bootstrap.py
    $ bin/buildout

You can now fetch a Youtube channel, and all recent videos will be downloaded
to the directory of your choice.  An Atom feed will also be dropped in the
directory, which will link directly to the downloaded files.

Here's an overview of what options you have::

    Usage: youtuber [options]

    Options:
    -h, --help            show this help message and exit
    -u YOUTUBE_USER, --user=YOUTUBE_USER
                            Youtube user name to download
    -d DEST_DIR, --dest=DEST_DIR
                            Directory to put videos and RSS feed
    -p PREFIX_URL, --prefix=PREFIX_URL
                            Prefix URL
    -b DAYS_BACK, --days-back=DAYS_BACK
                            Days back to download videos

And here's an example of downloading the past week's videos from
http://www.youtube.com/user/testedcom/featured::

    $ bin/youtuber --user=testedcom --prefix=http://www.example.com/
        --dest=/tmp/youtube --days-back=7

This will download all the videos uploaded by testedcom in the past week into
/tmp/youtube (unless they've already been downloaded).  It will also drop an
atom.xml in /tmp/youtube with links to all the downloaded videos (prefixed with
http://www.example.com/).  If you're running this on a web server, you'll want
this to be the web-reachable directory where the videos will be served from. If
you're running this locally, you'll probably want a file:// prefix.

I personally run this as a cron job on a web server to fetch new videos every
couple hours, and subscribe to the feed with my podcast client.  I also advise
running tmpwatch on the directory occasionally to delete old videos, especially
if storage becomes an issue.
