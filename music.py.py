from mingus.core import *
from mingus.midi import *
from mingus.containers import *
import os
import random
import copy
import math


def change_container_octave(nc, amount):
    """Given a note container, change octave of notes by 'amount'"""
    for note in nc:
        note.change_octave(amount)
    return nc

def print_track_note_containers(track):
    "Given a track, print all note containers"
    for i in range(0, len(track)):
        for j in range(0, len(track[i])):
            print(track[i][j][2])

def generate_melody(track_in, key, num_notes = 2):
    """Given a chord progression represented as a track, build a melody"""
    t = Track()
    melody_as_int = []
    melody = []
    scale = scales.get_notes(key)
    track = copy.deepcopy(track_in)

    # Get a basic skeleton of the melody by using notes of corresponding chords
    for i in range(0, len(track)):
        note = get_random_note_from_chord(chords.from_shorthand(track[i][0]))

        note = Note(note)
       # note.octave += 1

        melody.append(note)
        melody_as_int.append(int(note))

    # Fill in gaps between notes according to num_notes parameter
    for i in range(len(melody_as_int)-1, -1, -1):
        for j in range(1,num_notes):
            first_note = random.randint(melody_as_int[i]-8, melody_as_int[i] + 8)
            melody_as_int.insert(i, first_note)

    # Build a track with melody values in melody_as_int
    b = Bar()
    for i in range (0, len(melody_as_int)):

        n = Note()
        n.from_int(round_int_to_scale(melody_as_int[i], scale))

        if b.place_notes(n, num_notes) is False:
            t + b
            b = Bar()
            b.place_notes(n, num_notes)

    return t

def generate_chord_progression(key, length, arpeggio = False):
    """Given a key, build a chord progression of length number of bars"""
    t = Track()
    scale = scales.get_notes(key)
    t_sh = []

    for i in range (0, length):
        b = Bar()

        type = random.randint(1, 2)
        base = random.randint(0, 6)
        next_chord = []

        if type == 1:
            next_chord = chords.triads(key)[base]
        if type == 2:
            next_chord = chords.seventh(scale[base], key)

        if arpeggio:
            b = to_arpeggio(change_container_octave(NoteContainer(generate_random_inversion(next_chord)), -1))
        else:
            b.place_notes(change_container_octave(NoteContainer(generate_random_inversion(next_chord)), -1), 1)

        t_sh.append((NoteContainer(next_chord)).determine(True)[0])

        t + b

    return t, t_sh

def round_int_to_scale(int, scale):
    """Tunes a note to a scale by taking the ceiling of the integer value"""
    # pseudo
    s = copy.deepcopy(scale)
    s = [notes.note_to_int(n) for n in s]

    while int % 12 not in s:
        int = int + 1

    return int

def get_random_note_from_chord(chord):
    """Given a chord, get a random note from that chord"""
    num = random.randint(0, 3)
    while 1 == 1:

        if num == 3:
            if len(chord) == 4:
                return chord[num]
            else:
                num = random.randint(0,2)
        else:
            return chord[num]

def generate_random_inversion(chord):
    """Given a chord, generate a random inversion of that chord"""
    if len(chord) > 4 or len(chord) < 3:
        return "Error: chord must have only 3 or 4 notes"
    num = random.randint(1, 3)
    while 1 == 1:
        if num == 1:
            return chords.first_inversion(chord)
        if num == 2:
            return chords.second_inversion(chord)
        if num == 3:
            if len(chord) == 4:
                return chords.third_inversion(chord)
            else:
                num = random.randint(1, 2)

def to_arpeggio(chord):
    """Creates an arpeggio within a bar given a chord/note container. Assumes a 4x4 time signature"""
    b = Bar()
    if len(chord) == 3:
        third_note = copy.deepcopy(chord[0])
        third_note.octave +=1

        fourth_note = chord[1]
        fourth_note.octave += 1

        b.place_notes(chord[0], 4)
        b.place_notes(chord[2], 4)
        b.place_notes(third_note, 4)
        b.place_notes(fourth_note, 4)
    else:
        b.place_notes(chord[0], 4)
        b.place_notes(chord[1], 4)
        b.place_notes(chord[2], 4)
        b.place_notes(chord[3], 4)
    return b

def canon_progression(key, num_measures, arpeggio = False):
    """Builds a Canon Chord progession with random inversions for num_measures"""
    t = Track()
    for measure in range(0, num_measures):
        b = Bar()
        next_chord = []
        if measure % 8 == 0:
            next_chord = chords.I(key)
        if measure % 8 == 1:
            next_chord = chords.V(key)
        if measure % 8 == 2:
            next_chord = chords.VI(key)
        if measure % 8 == 3:
            next_chord = chords.III(key)
        if measure % 8 == 4:
            next_chord = chords.IV(key)
        if measure % 8 == 5:
            next_chord = chords.I(key)
        if measure % 8 == 6:
            next_chord = chords.IV(key)
        if measure % 8 == 7:
            next_chord = chords.V(key)

        #b.place_notes(change_container_octave(NoteContainer(generate_random_inversion(next_chord)), -1), 1)
        if arpeggio:
            b = to_arpeggio(change_container_octave(NoteContainer(next_chord), -1))
        else:
            b.place_notes(change_container_octave(NoteContainer(generate_random_inversion(next_chord)), -1), 1)

        t+b
    return t


def circle_progression(key, num_measures, arpeggio = False):
    t = Track()
    for measure in range(0, num_measures):
        b = Bar()
        next_chord = []
        if measure%8 == 0 or measure %8 == 7:
            next_chord = chords.I(key)
        if measure % 8 == 1:
            next_chord = chords.IV(key)
        if measure % 8 == 2:
            next_chord = chords.VII(key)
        if measure % 8 == 3:
            next_chord = chords.III(key)
        if measure % 8 == 4:
            next_chord = chords.VI(key)
        if measure % 8 == 5:
            next_chord = chords.II(key)
        if measure % 8 == 6:
            next_chord = chords.V(key)

        if arpeggio:
            b = to_arpeggio(change_container_octave(NoteContainer(next_chord), -1))
        else:
            b.place_notes(change_container_octave(NoteContainer(generate_random_inversion(next_chord)), -1), 1)

        t+b
    return t


def I_IV_V_I(key, measures):
    t = Track()
    for measure in range(0, measures):
        b = Bar()
        if measure%4 == 0:
            b.place_notes(NoteContainer(chords.I(key)), 1)
        if measure % 4 == 1:
            b.place_notes(change_container_octave(NoteContainer(chords.V(key)), -1), 1)
        if measure % 4 == 2:
            b.place_notes(change_container_octave(NoteContainer(chords.VI(key)),-1),1)
        if measure % 4 == 3:
            b.place_notes(change_container_octave(NoteContainer(chords.IV(key)),-1),1)

        t+b
    return t


def I_IV_V_I_bar(key):
    t = Track()
    b = Bar()
    b + (NoteContainer(chords.I(key)))

    b + change_container_octave(NoteContainer(chords.V(key)), -1)
    b + change_container_octave(NoteContainer(chords.VI(key)), -1)
    b + change_container_octave(NoteContainer(chords.IV(key)), -1)
    t + b
    return t

def generate_n_songs(n):
    """Generate n songs with a chord progression and melody"""
    major_keys = ['Cb', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F', 'C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#']
    minor_keys = ['ab', 'eb', 'bb', 'f', 'c', 'g', 'd', 'a', 'e', 'b', 'f#', 'c#', 'g#', 'd#', 'a#']
    for i in range(0, n):

        key = random.choice(major_keys)

        progression, shorthand = generate_chord_progression(key, 8, arpeggio = 0)
        melody = (generate_melody(shorthand, key, num_notes = 4))

        print("------------------")
        print("Song " + str(i))
        print("Key: ", key)
        print("Progression: ")
        print_track_note_containers(progression)
        print("Progression Shorthand: ", shorthand)
        print("Melody: ")
        print_track_note_containers(melody)

        song = Composition()
        song.add_track(progression)
        song.add_track(melody)


        filename = "test" + str(i) + ".midi"
        if os.path.exists(filename):
            os.remove(filename)
        midi_file_out.write_Composition(filename, song)


generate_n_songs(10)




