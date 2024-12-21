import os
import sys
import librosa
import numpy as np
from pydub import AudioSegment
import json
import shutil

def split_audio_on_transients(input_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    y, sr = librosa.load(input_file, sr=None)

    onset_env = librosa.onset.onset_strength(y=y, sr=sr)

  
    onset_frames = librosa.util.peak_pick(onset_env, pre_max=10, post_max=10, pre_avg=50, post_avg=50, delta=0.5, wait=10)


    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    onset_milliseconds = (onset_times * 1000).astype(int)


    min_duration = 200  # Minimum duration between transients (ms)
    filtered_onsets = [onset_milliseconds[0]]
    for onset in onset_milliseconds[1:]:
        if onset - filtered_onsets[-1] >= min_duration:
            filtered_onsets.append(onset)
    onset_milliseconds = np.array(filtered_onsets)


    audio = AudioSegment.from_file(input_file)
    onset_milliseconds = np.append(onset_milliseconds, len(audio))


    slices = []
    slice_durations = []
    for i in range(len(onset_milliseconds) - 1):
        start = onset_milliseconds[i]
        end = onset_milliseconds[i + 1]
        slice_audio = audio[start:end]
        slice_filename = f"{i+1}.wav"
        slice_path = os.path.join(output_dir, slice_filename)

        slice_audio.export(slice_path, format="wav")
        slices.append(slice_filename)
        slice_durations.append(len(slice_audio))  # Store slice duration in milliseconds

    return slices, slice_durations

def distribute_samples_to_main_folder(slices, slice_durations, output_base_dir):
    preset_count = 1
    slices_per_preset = 24
    total_slices = len(slices)
    
    while total_slices > 0:
        current_output_dir = f"{output_base_dir[:-7]}{preset_count}.preset"
        os.makedirs(current_output_dir, exist_ok=True)
        
        current_slices = slices[:slices_per_preset]
        current_durations = slice_durations[:slices_per_preset]
        slices = slices[slices_per_preset:]
        slice_durations = slice_durations[slices_per_preset:]
        total_slices = len(slices)
        
        regions = []
        for i, (slice_file, duration) in enumerate(zip(current_slices, current_durations)):
            slice_source_path = os.path.join(output_base_dir, slice_file)
            slice_dest_path = os.path.join(current_output_dir, slice_file)
            shutil.move(slice_source_path, slice_dest_path)
            
            region = {
                "sample": slice_file,
                "fade.in": 0,
                "fade.out": 0,
                "framecount": 10000 + i * 1000,
                "hikey": 53 + i,
                "lokey": 53 + i,
                "pan": 0,
                "pitch.keycenter": 60,
                "playmode": "oneshot",
                "reverse": False,
                "sample.end": 100000 + i * 100000,
                "transpose": 0,
                "tune": 0,
            }
            regions.append(region)
            
        # Generate patch.json for this preset
        patch_data = {
            "engine": {
                "bendrange": 8191,
                "highpass": 0,
                "modulation": {
                    "aftertouch": {"amount": 16383, "target": 0},
                    "modwheel": {"amount": 16383, "target": 0},
                    "pitchbend": {"amount": 16383, "target": 0},
                    "velocity": {"amount": 16383, "target": 0},
                },
                "params": [16384] * 8,
                "playmode": "mono",
                "portamento.amount": 0,
                "portamento.type": 32767,
                "transpose": 0,
                "tuning.root": 0,
                "tuning.scale": 0,
                "velocity.sensitivity": 19660,
                "volume": 18348,
                "width": 0,
            },
            "envelope": {
                "amp": {"attack": 0, "decay": 0, "release": 1000, "sustain": 32767},
                "filter": {"attack": 0, "decay": 3276, "release": 23757, "sustain": 983},
            },
            "fx": {
                "active": False,
                "params": [22014, 0, 30285, 11880, 0, 32767, 0, 0],
                "type": "ladder",
            },
            "lfo": {
                "active": False,
                "params": [20309, 5679, 19114, 15807, 0, 0, 0, 12287],
                "type": "random",
            },
            "octave": 0,
            "platform": "OP-XY",
            "regions": regions,
            "type": "drum",
            "version": 4,
        }
        
        with open(os.path.join(current_output_dir, "patch.json"), "w") as f:
            json.dump(patch_data, f, indent=4)
            
        preset_count += 1
        

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python xy.py <input_file> <output_dir>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2] + ".preset"

    slices, slice_durations = split_audio_on_transients(input_file, output_dir)
    distribute_samples_to_main_folder(slices, slice_durations, output_dir)

    print(f"Complete. Slices distributed and patch.json files created in {output_dir}.")
    
