import pygame
import os
import sys

pygame.mixer.pre_init(44100, -16, 2, 1024)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class AudioManager:
    
    def __init__(self):
        self.sounds = {}
        self.base_path = resource_path(os.path.join("assets", "audio"))
        
        pygame.mixer.set_num_channels(16)
        
        self.footstep_channel = pygame.mixer.Channel(0)
        self.pulse_channel = pygame.mixer.Channel(1)
        self.enemy_channel = pygame.mixer.Channel(2)
        
        self.load_assets()


    def load_assets(self):
        try:
            self.sounds['pulse'] = pygame.mixer.Sound(os.path.join(self.base_path, "pulse.wav"))
            self.sounds['footsteps'] = pygame.mixer.Sound(os.path.join(self.base_path, "footsteps.wav"))
            self.sounds['enemy'] = pygame.mixer.Sound(os.path.join(self.base_path, "enemy.flac"))
            self.sounds['key_found'] = pygame.mixer.Sound(os.path.join(self.base_path, "key_found.flac"))
            self.sounds['level_finish'] = pygame.mixer.Sound(os.path.join(self.base_path, "level_finish.wav"))
            self.sounds['chime_wall_hit'] = pygame.mixer.Sound(os.path.join(self.base_path, "chime_wall_hit.wav"))
            
            print("Audio assets loaded successfully.")
        except pygame.error as e:
            print(f"Error loading sounds: {e}. Check if file extensions (.wav vs .flac) match.")


    def play_pulse(self, distance_factor):
        if 'pulse' in self.sounds:
            volume = max(0.1, 1.0 - (distance_factor / 500))
            self.sounds['pulse'].set_volume(volume)
            self.pulse_channel.stop()
            self.pulse_channel.play(self.sounds['pulse'])


    def play_effect(self, sound_name, volume=1.0):
        if sound_name in self.sounds:
            if sound_name == 'footsteps':
                self.sounds['footsteps'].set_volume(volume)
                if not self.footstep_channel.get_busy():
                    self.footstep_channel.play(self.sounds['footsteps'])
            elif sound_name == 'enemy':
                self.sounds['enemy'].set_volume(volume)
                if not self.enemy_channel.get_busy():
                    self.enemy_channel.play(self.sounds['enemy'])
            else:
                self.sounds[sound_name].set_volume(volume)
                self.sounds[sound_name].play()