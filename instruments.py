#!/usr/bin/env python
from __future__ import division
import Nsound
from random import random
import collections

class Koto():
    "Nsound-compatible plucked-string instrument based on Karplus-Strong"
    def __init__(self,samplerate):
        self.samplerate = samplerate
    def play(self,duration,frequency):
        samplerate = self.samplerate
        if not frequency: return Nsound.Buffer.zeros(int(samplerate*duration))
        out = Nsound.AudioStream(samplerate,1) # mono
        cycles = int(samplerate/frequency)
        ring = collections.deque(Nsound.Buffer.rand(cycles).toList())
        for i in xrange(int(samplerate*duration)):
            out << ring[0]
            avg = 0.996*0.5*(ring[0] + ring[1])
            ring.append(avg)
            ring.popleft()
        return 0.25*out

