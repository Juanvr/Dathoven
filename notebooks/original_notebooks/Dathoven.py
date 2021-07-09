import glob, os
from keras.preprocessing.sequence import pad_sequences
from random import randint
import numpy as np
from music21 import converter, corpus, instrument, midi, note, chord, pitch, stream, interval, duration

def get_stream_from_midi_without_drums(midi_path):
    mf = midi.MidiFile()
    mf.open(midi_path)
    mf.read()
    mf.close()
    
    for i in range(len(mf.tracks)):
        mf.tracks[i].events = [ev for ev in mf.tracks[i].events if ev.channel != 10]          

    return midi.translate.midiFileToStream(mf)

def stream_to_array_of_pitches_strings (stream):
    result = []
    for element in stream.flat.notes:
        stringRepresentationOfElement = ''
        if isinstance(element, note.Note):
            stringRepresentationOfElement = element.pitch.ps
        else: # it's a chord
            stringRepresentationOfElement = [note.pitch.ps for note in element.notes][0]
            #stringRepresentationOfElement = ' '.join(listOfNotesWithOctaves)
        result.append(stringRepresentationOfElement)
    return result

def from_midi_to_array_of_pitches (midi_path):
    return stream_to_array_of_pitches_strings(get_stream_from_midi_without_drums(midi_path))

def from_pitches_to_intervals (array_of_pitches):
    intervals = []
    for i in range(1,len(array_of_pitches) - 1):
        intervals.append(array_of_pitches[i] - array_of_pitches[i-1])
    return intervals

def from_midi_to_array_of_intervals(midi_path):
    return from_pitches_to_intervals(from_midi_to_array_of_pitches(midi_path))

def get_folder_songs_intervals(folder_path):
    songs = []
    for file in glob.glob(folder_path):
        songs.append(from_midi_to_array_of_intervals(file))
    return songs

def from_array_of_intervals_to_pitches (root_pitch, intervals):
    pitches = [root_pitch]
    for interval in intervals:
        pitches.append(pitches[-1] + interval)
    return pitches

def from_pitches_to_midi (pitches, midi_path):
    streamResult = stream.Stream()
    for pitch in pitches:
            streamResult.append(note.Note(pitch))
            
    streamResult.write('midi', fp= midi_path)
    
def from_intervals_to_midi( root_pitch, intervals, midi_path):
    pitches = from_array_of_intervals_to_pitches(root_pitch, intervals)
    from_pitches_to_midi(pitches, midi_path)


def sample(preds):
    sorted_indexes = np.argsort(preds)[::-1]
    return sorted_indexes[randint(0,3)]

def sample_seq( seq, seq_length, model, output_seq_length ):
    if output_seq_length <= len(seq): raise Exception("output_seq_length must be higher than seq_length")
        
    output_seq = seq
    for i in range(output_seq_length - len(seq)):
        input_sequence = [seq[-seq_length:]]
        x = pad_sequences(input_sequence, maxlen = seq_length, padding="pre")
        prediction = model.predict(x)
        index = sample(prediction[0])
        output_seq.append(index)
    #[number_to_note(number) for number in output_seq]
    return output_seq


def stream_to_array_of_pitches_with_time (stream):
    result = []
    offsets = []
    for item in stream.flat.notes:
        element = []
        if isinstance(item, note.Note):
            element = item
        else: # it's a chord
            #pitch = [note.pitch.ps for note in element.notes][0]
            element = item.notes[0]
        
        resultElement = {
            'absolute_offset': element._getOffset(), 
            'pitch': element.pitch.ps, 
            'duration': element.duration.quarterLength if element.duration.quarterLength >0 else 1,
            'element': element
        }
        
        if not resultElement['absolute_offset'] in offsets:  # only keep one note per time position
            if not resultElement['duration'] == 0:
                result.append(resultElement)
                offsets.append(resultElement['absolute_offset'])
    result.sort(key=lambda x: x['absolute_offset'])
    return result

def from_midi_to_array_of_pitches_with_time (midi_path):
    return stream_to_array_of_pitches_with_time(get_stream_from_midi_without_drums(midi_path))

def from_pitches_to_intervals_with_time (array_of_pitches_with_time):
    intervals_with_time = []
    for i in range(1,len(array_of_pitches_with_time) - 1):
        first_element = array_of_pitches_with_time[i-1]
        second_element = array_of_pitches_with_time[i]
        resultElement = {
            'relative_offset': second_element['absolute_offset'] - first_element['absolute_offset'],
            'interval': second_element['pitch'] - first_element['pitch'],
            'duration': second_element['duration']
        }
        intervals_with_time.append(resultElement)
    return intervals_with_time

def from_midi_to_array_of_intervals_with_time(midi_path):
    return from_pitches_to_intervals_with_time(from_midi_to_array_of_pitches_with_time(midi_path))

def get_folder_songs_intervals_with_time(folder_path):
    songs = []
    for file in glob.glob(folder_path):
        songs.append(from_midi_to_array_of_intervals_with_time(file))
    return songs

    
def from_array_of_intervals_to_pitches_with_time (root_pitch, intervals_with_time):
    elements = [{
            'absolute_offset': 0, 
            'pitch': root_pitch, 
            'duration': 1
        }]
    for interval in intervals_with_time:
        previousElement = elements[-1]
        resultElement = {
            'absolute_offset': previousElement['absolute_offset'] + interval['relative_offset'], 
            'pitch': previousElement['pitch'] + interval['interval'], 
            'duration': interval['duration'],
        }
        elements.append(resultElement)
    return elements

def from_pitches_with_time_to_midi (pitches_with_time, midi_path):
    streamResult = stream.Stream()
    for pitch_with_time in pitches_with_time:
        element = note.Note(pitch_with_time['pitch'])
        element._setOffset(pitch_with_time['absolute_offset'])
        d = duration.Duration()
        d.quarterLength = pitch_with_time['duration']
        element.duration = d
        streamResult.append(element)
            
    streamResult.write('midi', fp= midi_path)
    
def from_intervals_with_time_to_midi( root_pitch, intervals, midi_path):
    pitches_with_time = from_array_of_intervals_to_pitches_with_time(root_pitch, intervals)
    from_pitches_with_time_to_midi(pitches_with_time, midi_path)