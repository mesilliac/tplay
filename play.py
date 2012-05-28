#!/usr/bin/env python
import math
import Nsound
# setup
samplerate = 44100 # per second
nchannels = 2 # per sample
bits = 16 # per channel?
clipping_freq = 16.0
sine = Nsound.Sine(samplerate)
# playback
out = Nsound.AudioStream(samplerate,nchannels)
playback = Nsound.AudioPlayback(samplerate,nchannels,bits)
# instruments
bass = Nsound.GuitarBass(samplerate)
organ = Nsound.OrganPipe(samplerate) # requires dual channel output
clarinet = Nsound.Clarinet(samplerate)
kicker = Nsound.DrumKickBass(samplerate,1000,40)
bd01 = Nsound.DrumBD01(samplerate)
hat = Nsound.Hat(samplerate)
flute = Nsound.FluteSlide(samplerate)

# play a given melody with the given timing
def play(melody,timing,bpm=200,swing=False,transpose=0,instrument=bass):
    """play(melody,timing,bpm=200,swing=False,transpose=0,instrument=bass):
    melody = [pitch,pitch,pitch,...]
    timing = ('.' + ' ' * (len(note)-1)) * len(song)
    bpm = beats per minute
    swing = play two beats as 2+1 beats
    transpose = number of semitones to transpose by (12 = 1 octave)
    instrument = Nsound-compatible instrument to use
    """
    if not timing: timing = '.' * len(melody)
    if transpose: pitch_multiplier = 2**(transpose/12.0)
    beat_length = 60.0 / bpm
    if swing: beat_length /= 1.5
    playhead = 0
    for pos in xrange(len(timing)):
        beat = timing[pos]
        if beat.isspace(): continue
        duration = 1
        if swing and not pos % 2: duration += 1
        for x in xrange(pos+1,len(timing)):
            if not timing[x].isspace(): break
            duration += 1
            if swing and not x % 2: duration += 1
        if playhead < len(melody): pitch = melody[playhead]
        if transpose: pitch *= pitch_multiplier
        duration *= beat_length
        playhead += 1
        yield instrument.play(duration,pitch) / math.log(pitch/clipping_freq,2)

# play something once
def play_once(*args,**kwargs):
    for sample in play(*args,**kwargs): sample >> playback

# play something more than once
def loop(*args,**kwargs):
    """loop(*args,**kwargs,alternate_swing=False,repeat=1)"""
    try: alternate = kwargs.pop('alternate_swing')
    except KeyError: alternate = False
    try: repeat = kwargs.pop('repeat')
    except KeyError: repeat = -1
    while repeat:
        if not alternate: play_once(*args,**kwargs)
        else:
            kwargs['swing'] = False
            play_once(*args,**kwargs)
            kwargs['swing'] = True
            play_once(*args,**kwargs)
        repeat -= 1

# notes for melody use
a4 = 440.00
# (note)(octave) = (a4)*2**(octave-4)*2**(note-a)
for octave in range(8):
    for key,count in zip(['c','cs','d','ds','e','f','fs','g','gs','a','as','b'],range(12)):
        exec(str(key)+str(octave)+' = a4*2**'+str((octave-4)+(count-9)/12.0))

# some test melodies tommy made up
m1  = [c1,g1,a1,g1,a1,b1,c2,g1,a1,g1,a1,b1,c2,g1,a1,g1,e1,d1,g1,e1,d1]
t1  = '. . . ..... . ..... . ...    ...'
#
m2a = [c2,d2,e2,d2,c2,b1,c2]
t2a = '....... '
m2b = [c2,d2,e2,d2,c2,c3,c2]
t2b = '....... '
m2 = m2a + m2b
t2 = t2a + t2b
#
m3a = [c2,c3,c2,b1,c2,a2,f1,e1,d1,g1,e1,d1]
t3a = '.........    ...'
m3b = [c1,c3,c2,b2,c2,a2,f1,e1,d1,g1,e1,d1]
t3b = '.........    ...'
#
m4a = [a1,b1,c2]*4
t4a = '. . . .. .......'
m4b = [f1,g1,a1]*4
t4b = t4a
m4c = [e1,gs1,a1,e1,e1,f1,e1,d1,c1,b0]
t4c = '. . . ..   .....'
m4d = [a0,b0,c1,d1,e1,f1,e1,f1,e1,f1,e1,f1]
t4d = '. . . .. .......'
m4 = m4a + m4b + m4c + m4d
t4 = t4a + t4b + t4c + t4d
#
m5  = [a1,c2,a1,c2,a1,gs2,a2,c2,g2,f2,a1,e2]
t5  = '.   .  .. .     .   .  .. . . . '
#
m6  = [a1,b1,c2,d2,e2,ds2,e2,f2,e2]
t6  = '.   .   .   .   .      .. .   . '
#
m7  = [a1,e2,ds2,e2,c2,b1,c2,a1,g1,b1,c2,d2,c2,b1]
t7  = '.   .  .. .   ...   .  .. .  .. '

# timing, currently unused except for fade-in
crotchet = 0.7 # seconds
quaver = crotchet / 2**1
semiquaver = crotchet / 2**2
minim = crotchet * 2**1
bar = crotchet * 2**2

# play some test melodies
def play_test_melodies():
    # ensure clean fade-in
    sine.silence(quaver) >> playback
    try:
        loop(m1,t1, transpose=12, repeat=2)
        loop(m2,t2,bpm=200,transpose=0,alternate_swing=True,repeat=1)
        loop(m3a,t3a,swing=True,repeat=1)
        loop(m3b,t3b,swing=True,repeat=1)
        loop(m4,t4,swing=True,repeat=2)
        loop(m5,t5,repeat=1)
        loop(m6,t6,bpm=133*2,transpose=2,repeat=2)
        loop(m7,t7,repeat=2)
        loop(m4,t4)
    except KeyboardInterrupt: exit()

def play_bugle_song():
    t = '...     ...     ... ... ...     ...     ...     ...             '
    m = [g2,g2,c3,g2,c3,e3,g2,c3,e3,g2,c3,e3,g2,c3,e3,g3,e3,c3,e3,c3,g2,g2,g2,c3]
    loop(m,t,swing=True)

# parse and play from command line
def play_from_command_line():
    from optparse import OptionParser
    options, args = OptionParser().parse_args()
    if not args: play_test_melodies(); exit()
    print(args)
    song = args[0]
    play_song(song)

# play a song
def play_song(song="045[4567]45[4567]45[421~~~][.421]", root=a1, mode='major', speed=100.0, loop=True):
    spb = 60.0/speed # seconds per beat
    sine.silence(spb*1) >> playback
    t = lambda a,b: a*2**(b/12.0)
    if mode == 'major':
        scale = [root,t(root,2),t(root,4),t(root,5),t(root,7),t(root,9),t(root,11),t(root,12)]
    if mode == 'minor':
        scale = [root,t(root,2),t(root,3),t(root,5),t(root,7),t(root,8),t(root,10),t(root,12)]
    def get_note_length(playhead):
        note = song[playhead]
        assert note.isdigit()
        duration = 1
        while playhead < len(song)-1:
            playhead += 1
            char = song[playhead]
            if char == '~' or char.isspace(): duration += 1
            else: break
        return duration
    note = None
    playhead = -1
    try:
        while playhead < len(song):
            playhead += 1
            if playhead == len(song) and loop: playhead = -1; continue
            char = song[playhead]
            if char.isdigit(): # new note
                freq = scale[int(char)]
                length = get_note_length(playhead)
                note = (spb*length, freq)
            elif char.isspace(): continue # do whatever
            elif char == '~': continue # sustain note
            elif char == '.': note = (spb, 0)
            elif char == '[': spb /= 2; continue
            elif char == ']': spb *= 2; continue
            elif char == '(': spb *= 2; continue
            elif char == ')': spb /= 2; continue
            if note[1]: bass.play(*note) / math.log(pitch/clipping_freq,2) >> playback
            else: sine.silence(note[0]) >> playback
    except KeyboardInterrupt: pass

# if running standalone
if __name__ == "__main__": play_from_command_line()

