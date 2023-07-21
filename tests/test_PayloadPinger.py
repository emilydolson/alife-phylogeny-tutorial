import time

import pylib


def test_PayloadPinger_same():
    for _attempt in range(20):
        pinger = pylib.PayloadPinger()
        pinger.send("google.com", "payload1")
        pinger.send("google.com", "payload2")

        time.sleep(2)

        if {pinger.read(), pinger.read(),} == {
            "payload1",
            "payload2",
        }:
            break
    else:
        assert False


def test_PayloadPinger_slowfast():
    for _attempt in range(20):
        pinger = pylib.PayloadPinger()
        pinger.send("google.com", "payload1")
        pinger.send("127.0.0.1", "payload2")

        time.sleep(2)

        if {pinger.read(), pinger.read(),} == {
            "payload2",
            "payload1",
        }:
            break
    else:
        assert False


def test_PayloadPinger_fastslow():
    for _attempt in range(20):
        pinger = pylib.PayloadPinger()
        pinger.send("127.0.0.1", "payload1")
        pinger.send("google.com", "payload2")

        time.sleep(2)

        if {pinger.read(), pinger.read(),} == {
            "payload1",
            "payload2",
        }:
            break
    else:
        assert False
