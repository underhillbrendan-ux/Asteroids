import os
import numpy as np
import pygame

# Point Pygame to the WSLg PulseAudio socket BEFORE importing pygame
os.environ['PULSE_SERVER'] = 'unix:/mnt/wslg/PulseServer'
os.environ['SDL_AUDIODRIVER'] = 'pulseaudio'


def init_audio(sample_rate=44100, buffer_size=512):
    """Initializes Pygame audio mixer with low buffer size to eliminate WSLg latency."""
    if not pygame.mixer.get_init():
        try:
            pygame.mixer.pre_init(frequency=sample_rate, size=-16, channels=2, buffer=buffer_size)
            pygame.mixer.init()
           
        except pygame.error as e:
            print(f"Audio initialization failed: {e}")


def generate_laser_sound(
    start_freq=800, end_freq=150, duration=0.2, volume=0.2
) -> pygame.mixer.Sound:
    init_audio()
    sample_rate = 44100

    total_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, total_samples, False)

    freqs = np.linspace(start_freq, end_freq, total_samples)
    phase = 2 * np.pi * np.cumsum(freqs) / sample_rate
    wave = np.sin(phase)

    envelope = np.exp(-3 * t / duration)
    attack_samples = int(sample_rate * 0.003)
    envelope[:attack_samples] *= np.linspace(0, 1, attack_samples)

    wave = wave * envelope
    audio_data = (wave * 32767 * volume).astype(np.int16)
    stereo_audio = np.column_stack((audio_data, audio_data))

    return pygame.mixer.Sound(buffer=stereo_audio)


def generate_explosion_sound(
    start_freq=250, end_freq=30, duration=0.4, volume=0.4
) -> pygame.mixer.Sound:
    init_audio()
    sample_rate = 44100

    total_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, total_samples, False)

    freqs = np.linspace(start_freq, end_freq, total_samples)
    phase = 2 * np.pi * np.cumsum(freqs) / sample_rate
    rumble = np.sin(phase)

    noise = np.random.uniform(-0.8, 0.8, total_samples)
    wave = (rumble * 0.4) + (noise * 0.6)

    envelope = np.exp(-4.5 * t / duration)
    attack_samples = int(sample_rate * 0.003)
    envelope[:attack_samples] *= np.linspace(0, 1, attack_samples)

    wave = wave * envelope
    audio_data = (wave * 32767 * volume).astype(np.int16)
    stereo_audio = np.column_stack((audio_data, audio_data))

    return pygame.mixer.Sound(buffer=stereo_audio)


class SoundManager:
    # Loads sound once
    def __init__(self):
        init_audio()
        self.laser = generate_laser_sound()
        self.explosion = generate_explosion_sound()


# Single instance shared across your modules
sound_manager = SoundManager()
