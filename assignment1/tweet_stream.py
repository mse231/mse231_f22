#!/usr/bin/env python3
"""Collect tweets from Twitter streaming API via tweepy"""

import argparse
import datetime
import gzip
import os
import sys
import time

from tweepy import Stream, Client, StreamingClient, StreamRule, Paginator


class CustomStreamingClient(StreamingClient):
    def __init__(self, write=print, **kwds):
        super(CustomStreamingClient, self).__init__(**kwds)
        self.write = write

    def on_tweet(self, tweet):
        self.write(tweet.data)

    def on_data(self, raw_data):
        self.write(raw_data)

    def on_error(self, status_code):
        eprint(status_code)


def eprint(*args, **kwargs):
    """Print to stderr"""
    print(*args, file=sys.stderr, **kwargs)


if __name__ == "__main__":
    # Set up the argument parser
    parser = argparse.ArgumentParser(
        description="Fetch data with Twitter Streaming API"
    )
    parser.add_argument("--keyfile", help="file with user credentials", required=True)
    parser.add_argument(
        "--gzip", metavar="OUTPUT_FILE", help="file to write compressed results to"
    )
    parser.add_argument(
        "--filter",
        metavar="W",
        nargs="*",
        help="space-separated list of words;"
        "tweets matching any word in the list are returned",
    )
    flags = parser.parse_args()

    # Read twitter app credentials and set up authentication
    creds = {}
    for line in open(flags.keyfile, "r"):
        row = line.strip()
        if row:
            key, value = row.split()
            creds[key] = value

    twitterstream = Stream(
        creds["api_key"], creds["api_secret"], creds["token"], creds["token_secret"]
    )

    # Write tweets to stdout or a gzipped file, as requested
    if flags.gzip:
        # Write to gzipped file
        f = gzip.open(flags.gzip, "wb")
        eprint("Writing gzipped output to %s" % flags.gzip)
        sep = os.linesep.encode()
        output = lambda x: f.write(x + sep)
    else:
        # write to stdout
        output = print

    # Track time and start streaming
    starttime = datetime.datetime.now()
    twitter_streaming_client = CustomStreamingClient(write=output, bearer_token=creds["bearer_token"])
    twitter_client = Client(bearer_token=creds["bearer_token"])
    eprint("Started running at", starttime)

    try:
        if flags.filter:
            # Track specific tweets
            query = " ".join(flags.filter) + " lang:en"
            twitter_streaming_client.add_rules(StreamRule(query))
            twitter_streaming_client.filter()
        else:
            # Sample random tweets
            while True:
                time.sleep(0.1)
                twitter_streaming_client.sample()
    except KeyboardInterrupt:
        eprint()
    except AttributeError:
        # Catch rare occasion when Streaming API returns None
        pass

    if flags.gzip:
        eprint("Closing %s" % flags.gzip)
        f.close()

    eprint("Total run time", datetime.datetime.now() - starttime)

