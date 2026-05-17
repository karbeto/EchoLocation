import pygame
import os

pygame.mixer.pre_init(44100, -16, 2, 512)

class AudioManager:
    
    def __init__(self):
        self.sounds = {}
        self.base_path = os.path.join("assets", "audio")
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
        volume = max(0.1, 1.0 - (distance_factor / 500))
        self.sounds['pulse'].set_volume(volume)
        self.sounds['pulse'].play()


    def play_effect(self, sound_name, volume=1.0):
        if sound_name in self.sounds:
            self.sounds[sound_name].set_volume(volume)
            self.sounds[sound_name].play()