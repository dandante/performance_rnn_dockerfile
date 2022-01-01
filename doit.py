#!/usr/bin/env python3

# Hack to allow python to pick up the newly-installed fluidsynth lib.
import ctypes.util
orig_ctypes_util_find_library = ctypes.util.find_library
def proxy_find_library(lib):
  if lib == 'fluidsynth':
    return 'libfluidsynth.so.2'
  else:
    return orig_ctypes_util_find_library(lib)
ctypes.util.find_library = proxy_find_library

import os
from magenta.models.performance_rnn import performance_sequence_generator
from magenta.models.shared import sequence_generator_bundle
from note_seq.protobuf import generator_pb2
from note_seq.protobuf import music_pb2

import note_seq

# Necessary until pyfluidsynth is updated (>1.2.5).
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Constants.
BUNDLE_DIR = '/tmp/'
MODEL_NAME = 'performance_with_dynamics'
BUNDLE_NAME = MODEL_NAME + '.mag'

bundle = sequence_generator_bundle.read_bundle_file(os.path.join(BUNDLE_DIR, BUNDLE_NAME))
generator_map = performance_sequence_generator.get_generator_map()
generator = generator_map[MODEL_NAME](checkpoint=None, bundle=bundle)
generator.initialize()
generator_options = generator_pb2.GeneratorOptions()
generator_options.args['temperature'].float_value = 1.0  # Higher is more random; 1.0 is default. 
generate_section = generator_options.generate_sections.add(start_time=0, end_time=30)
sequence = generator.generate(music_pb2.NoteSequence(), generator_options)

# Play and view this masterpiece.
note_seq.plot_sequence(sequence)
note_seq.play_sequence(sequence, note_seq.midi_synth.fluidsynth,
                 sf2_path='/tmp/Yamaha-C5-Salamander-JNv5.1.sf2')
note_seq.note_sequence_to_midi_file(sequence, "/work/foo.mid")