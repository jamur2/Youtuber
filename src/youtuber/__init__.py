import bottle
import datetime
import feedparser
import optparse
import os
import subprocess
import urlparse

youtube_prefix = "http://gdata.youtube.com/feeds/api/users/"
youtube_suffix = "/uploads?orderby=updated"

res_1080p = '37'
res_720p = '22'

# Template modified from original at
# http://stackoverflow.com/questions/5916375/serializing-a-feedparser-object-to-atom/5916461#5916461
# All credit to namsral

feed_template = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
    <title>{{! d['title'] }}</title>
    <id>{{! d['id'] }}</id>
    <updated>{{! d['updated'] }}</updated>
    %for entry in entries:
    <entry>
        <title>{{! entry['title'] }}</title>
        <link rel="enclosure" type="video/mpeg" href="{{! entry['links'][0]['href'] }}" />
        <id>{{! entry['id'] }}</id>
        <published>{{! entry['published'] }}</published>
        <updated>{{! entry['updated'] }}</updated>
        <author>
            <name>{{! d['author'] }}</name>
        </author>
        <content type="{{! entry['content'][0]['type'] }}" xml:lang="en">
            <![CDATA[{{! entry['content'][0].value }}]]>
        </content>
    </entry>
    %end

</feed>
"""

def download_video(vid_id, dest_dir):
    dest_path = os.path.join(dest_dir, vid_id + '.mp4')
    if not os.path.exists(dest_path):
        cmd = ("youtube-dl http://youtube.com/watch?v=" + vid_id + " -o " +
            dest_path + " -f " + res_1080p)
        p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
        output = p.stdout.read()
        if 'requested format not available' in output:
            cmd = cmd.replace(res_1080p, res_720p)
            p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
            output = p.stdout.read()
    return dest_path


def main():
    parser = optparse.OptionParser()
    parser.add_option("-u", "--user", dest="youtube_user",
        help="Youtube user name to download")
    parser.add_option("-d", "--dest", dest="dest_dir",
        help="Directory to put videos and RSS feed")
    parser.add_option("-p", "--prefix", dest="prefix_url",
        help="Prefix URL")
    parser.add_option("-b", "--days-back", dest="days_back",
        help="Days back to download videos")
    (options, args) = parser.parse_args()
    youtube_user = options.youtube_user
    dest_dir = options.dest_dir
    prefix_url = options.prefix_url
    days_back = int(options.days_back)
    youtube_url = youtube_prefix + youtube_user + youtube_suffix
    contents = feedparser.parse(youtube_url)
    for entry_index in range(len(contents.entries)):
        entry = contents.entries[entry_index]
        for link_index in range(len(entry.links)):
            link = entry.links[link_index]
            if 'watch' in link.href:
                vid_id = urlparse.parse_qs(
                    urlparse.urlparse(link.href)[4])['v'][0]
                contents['entries'][entry_index]['links'][link_index]['href'] = prefix_url + vid_id + '.mp4'
                if (datetime.datetime(*entry.published_parsed[:6]) >
                        datetime.datetime.now() -
                        datetime.timedelta(days=days_back)):
                    download_video(vid_id, dest_dir)
    fi = open(os.path.join(dest_dir, 'atom.xml'), 'w')
    fi.write(bottle.template(
        feed_template, {'d': contents.feed, 'entries': contents.entries}))
    fi.close()


if __name__ == '__main__':
    main()

