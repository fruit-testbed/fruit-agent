#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import syslog

CONFIG_FILES = os.environ.get('FRUIT_AGENT_CONFIG_FILES',
                              '/run/fruit.json@local:/run/fruit.json@server').split(':')

__config_blobs = None

def _get(path, blob, default=None):
    if path == '':
        return blob

    if path[:1] != '/':
        raise ValueError('Invalid jsonpointer: %r' % (path,))

    for piece in path.split('/')[1:]:
        piece = piece.replace('~1', '/')
        piece = piece.replace('~0', '~')
        if isinstance(blob, dict):
            if piece not in blob:
                return default
            blob = blob[piece]
        elif isinstance(blob, list):
            try:
                blob = blob[int(piece, 10)]
            except ValueError:
                return default  ## non-integer key --> definitely not present!
            except IndexError:
                return default  ## out-of-range key --> not present
        else:
            return default  ## non-indexable value

    return blob

def clear_cache():
    global __config_blobs
    __config_blobs = None

__sentinel = object()
def get(path, default=None):
    global __config_blobs
    if __config_blobs is None:
        __config_blobs = []
        for filename in CONFIG_FILES:
            if os.path.exists(filename):
                try:
                    with open(filename, 'rt') as fh:
                        __config_blobs.append(json.load(fh))
                except:
                    syslog.syslog(syslog.LOG_WARNING,
                                  'Could not load fruit config file %r' % (filename,))
    for blob in __config_blobs:
        v = _get(path, blob, default=__sentinel)
        if v is not __sentinel:
            return v
    return default
