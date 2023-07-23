import time

import pylib


def test_PayloadPinger_same():
    for _attempt in range(20):
        pinger = pylib.PayloadPinger()
        pinger.send("google.com", "payload1".encode())
        pinger.send("google.com", "payload2".encode())

        time.sleep(2)

        if {pinger.read().decode(), pinger.read().decode(),} == {
            "payload1",
            "payload2",
        }:
            break
    else:
        assert False


def test_PayloadPinger_slowfast():
    for _attempt in range(20):
        pinger = pylib.PayloadPinger()
        pinger.send("google.com", "payload1".encode())
        pinger.send("127.0.0.1", "payload2".encode())

        time.sleep(2)

        if {pinger.read().decode(), pinger.read().decode(),} == {
            "payload2",
            "payload1",
        }:
            break
    else:
        assert False


def test_PayloadPinger_fastslow():
    for _attempt in range(20):
        pinger = pylib.PayloadPinger()
        pinger.send("127.0.0.1", "payload1".encode())
        pinger.send("google.com", "payload2".encode())

        time.sleep(2)

        if {pinger.read().decode(), pinger.read().decode(),} == {
            "payload1",
            "payload2",
        }:
            break
    else:
        assert False
