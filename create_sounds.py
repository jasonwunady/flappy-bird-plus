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

def create_background_music():
    sample_rate = 44100
    duration = 0.2  # Duration of each note
    
    # Create time array for a single note
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Define frequencies for a simple tune (E5, E5, E5, C5, G5)
    frequencies = [659.25, 659.25, 659.25, 523.25, 783.99]
    notes = []
    
    # Generate each note
    for freq in frequencies:
        # Generate the note
        note = 0.3 * np.sign(np.sin(2 * np.pi * freq * t))  # Square-ish wave
        notes.append(note)
        
        # Add small silence between notes
        silence = np.zeros(int(sample_rate * 0.1))
        notes.append(silence)
    
    # Combine all notes into one array
    complete_sound = np.concatenate(notes)
    
    # Normalize and convert to 16-bit integer
    complete_sound = np.int16(complete_sound / np.max(np.abs(complete_sound)) * 32767)
    
    # Save the sound
    wavfile.write('sounds/background.wav', sample_rate, complete_sound)
    
    # Normalize and convert to 16-bit integer
    sound = np.int16(sound / np.max(np.abs(sound)) * 32767)
    
    # Save the sound
    wavfile.write('sounds/background.wav', sample_rate, sound)

if __name__ == '__main__':
    create_wing_sound()
    create_background_music()