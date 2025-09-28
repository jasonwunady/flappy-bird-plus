import numpy as np
from scipy.io import wavfile

def create_wing_sound():
    # Create a short "wing flap" sound
    sample_rate = 44100
    duration = 0.1
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Create a sound that goes from high to low frequency
    frequency = np.linspace(1000, 400, len(t))
    sound = np.sin(2 * np.pi * frequency * t)
    
    # Apply envelope
    envelope = np.exp(-t * 30)
    sound = sound * envelope
    
    # Normalize and convert to 16-bit integer
    sound = np.int16(sound * 32767)
    
    # Save the sound
    wavfile.write('sounds/wing.wav', sample_rate, sound)

def create_mario_note(frequency, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = 0.3 * np.sign(np.sin(2 * np.pi * frequency * t))
    envelope = 1.0 - 0.1 * t/duration  # Linear decay
    return wave * envelope

def create_background_music():
    sample_rate = 44100
    note_duration = 0.2
    
    # Mario-like melody (E5, E5, E5, C5, G5)
    notes = [
        (659.25, note_duration),  # E5
        (659.25, note_duration),  # E5
        (659.25, note_duration),  # E5
        (523.25, note_duration),  # C5
        (783.99, note_duration * 1.5),  # G5
    ]
    
    # Generate the complete sound
    parts = []
    for freq, duration in notes:
        # Create note
        note = create_mario_note(freq, duration, sample_rate)
        parts.append(note)
        
        # Add small gap between notes
        gap = np.zeros(int(sample_rate * 0.05))
        parts.append(gap)
    
    # Combine all parts
    sound = np.concatenate(parts)
    
    # Normalize and convert to 16-bit integer
    sound = np.int16(sound / np.max(np.abs(sound)) * 32767)
    
    # Save the sound
    wavfile.write('sounds/background.wav', sample_rate, sound)

if __name__ == '__main__':
    create_wing_sound()
    create_background_music()