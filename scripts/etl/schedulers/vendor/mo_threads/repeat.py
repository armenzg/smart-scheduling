# encoding: utf-8
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Contact: Kyle Lahnakoski (kyle@lahnakoski.com)
#
from __future__ import division
from __future__ import unicode_literals

from mo_future import is_text
from mo_logs import Log
from mo_threads import Till
from mo_threads.signals import Signal
from mo_times import Duration, Date


class Repeat(object):

    def __init__(self, message="ping", every="second", start=None, until=None):

        if is_text(message):
            self.message = show_message(message)
        else:
            self.message = message

        self.every = Duration(every)

        if isinstance(until, Signal):
            self.please_stop = until
        elif until == None:
            self.please_stop = None
        else:
            self.please_stop = Till(Duration(until).seconds)

        if start:
            self.start = start
            self.next_time = self.start
            self.again()
        else:
            self.start = Date.now()

    def __enter__(self):
        self.start = Date.now()
        self.next_time = self.start
        self.please_stop = Signal()
        self.again()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.please_stop.go()

    def again(self):
        if self.please_stop:
            return
        self.message()
        self.next_time = self.next_time + self.every
        self.next = Till(till=self.next_time.unix)
        self.next.then(self.again)


def show_message(message):
    def output():
        Log.note(message)
    return output