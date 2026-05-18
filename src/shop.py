class ShopManager:
    def __init__(self):
        self.radius_level = 0
        self.cooldown_level = 0
        self.speed_level = 0 
        
        self.max_level = 5
        self.base_upgrade_cost = 20
        self.cost_multiplier = 1.5
        
        self.base_speed_cost = 30
        self.speed_cost_multiplier = 1.8


    def get_upgrade_cost(self, current_level, is_speed=False):
        if is_speed:
            return int(self.base_speed_cost * (self.speed_cost_multiplier ** current_level))
        return int(self.base_upgrade_cost * (self.cost_multiplier ** current_level))


    def get_radius_modifier(self):
        return 1.0 + (self.radius_level * 0.20)


    def get_cooldown_modifier(self):
        return 1.0 - (self.cooldown_level * 0.15)


    def get_speed_modifier(self):
        return 1.0 + (self.speed_level * 0.12)


    def try_upgrade_radius(self, current_xp):
        if self.radius_level >= self.max_level:
            print("Radius upgrade already at max tier!")
            return False, current_xp
            
        cost = self.get_upgrade_cost(self.radius_level)
        if current_xp >= cost:
            self.radius_level += 1
            print(f"Upgraded Radius to Tier {self.radius_level}!")
            return True, current_xp - cost
            
        print("Not enough XP for Radius upgrade!")
        return False, current_xp


    def try_upgrade_cooldown(self, current_xp):
        if self.cooldown_level >= self.max_level:
            print("Cooldown upgrade already at max tier!")
            return False, current_xp
            
        cost = self.get_upgrade_cost(self.cooldown_level)
        if current_xp >= cost:
            self.cooldown_level += 1
            print(f"Upgraded Cooldown to Tier {self.cooldown_level}!")
            return True, current_xp - cost
            
        print("Not enough XP for Cooldown upgrade!")
        return False, current_xp 


    def try_upgrade_speed(self, current_xp):
        if self.speed_level >= self.max_level:
            print("Speed upgrade already at max tier!")
            return False, current_xp
            
        cost = self.get_upgrade_cost(self.speed_level, is_speed=True)
        if current_xp >= cost:
            self.speed_level += 1
            print(f"Upgraded Player Speed to Tier {self.speed_level}!")
            return True, current_xp - cost
            
        print("Not enough XP for Speed upgrade!")
        return False, current_xp