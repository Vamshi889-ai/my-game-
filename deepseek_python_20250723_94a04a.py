# 🚗 ADAS Driving Game - Final Working Version
# [Click "Runtime" -> "Run all"] or press Ctrl+F9

# 1. Install dependencies
!pip install -q gtts pydub matplotlib
!apt-get -qq install ffmpeg

# 2. Import libraries
import numpy as np
import matplotlib.pyplot as plt
from gtts import gTTS
from IPython.display import Audio, display, clear_output
import time
import random

# 3. Game Engine
class ADASGame:
    def __init__(self):
        self.score = 100
        self.speed = 50
        self.distance = 0
        self.obstacles = []
        self.alerts = []
        self.start_time = time.time()
        
    def generate_obstacle(self):
        """Create random road obstacles"""
        obstacle_types = ['pedestrian', 'slow_car', 'red_light', 'curve']
        return {
            'type': random.choice(obstacle_types),
            'distance': self.distance + random.randint(50, 150),
            'speed_limit': random.choice([30, 40, 60])
        }
    
    def play(self):
        """Main game loop"""
        print("""
        ██████╗ ██████╗  █████╗ ██╗   ██╗███████╗
        ██╔══██╗██╔══██╗██╔══██╗██║   ██║██╔════╝
        ██║  ██║██████╔╝███████║██║   ██║███████╗
        ██║  ██║██╔══██╗██╔══██║██║   ██║╚════██║
        ██████╔╝██║  ██║██║  ██║╚██████╔╝███████║
        ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
        """)
        print("🚦 ADAS Driving Game Started!")
        print("Controls: [A]ccelerate, [B]rake, [C]ruise\n")
        
        # Generate first obstacle
        self.obstacles.append(self.generate_obstacle())
        
        while self.score > 0 and self.distance < 1000:
            clear_output(wait=True)
            self.display_status()
            
            # Check for obstacle hits
            self.check_obstacles()
            
            # Get player input
            action = input("Action (A/B/C): ").upper()
            
            # Update game state
            self.update_game(action)
            
            # Generate new obstacles
            if self.distance >= self.obstacles[-1]['distance'] - 20:
                self.obstacles.append(self.generate_obstacle())
            
            time.sleep(0.5)
        
        self.end_game()

    def update_game(self, action):
        """Process player actions"""
        if action == 'A':  # Accelerate
            self.speed = min(120, self.speed + 10)
            if self.speed > 80:
                self.score -= 2
        elif action == 'B':  # Brake
            self.speed = max(0, self.speed - 15)
            if self.speed < 30:
                self.score -= 1
        else:  # Cruise
            self.speed = max(30, self.speed - 2)
        
        self.distance += self.speed * 0.1
        
        # Random events
        if random.random() < 0.1:
            self.score -= 5
            self.alerts.append("Distracted driving!")
    
    def check_obstacles(self):
        """Handle obstacle collisions"""
        for obs in self.obstacles[:]:
            if abs(self.distance - obs['distance']) < 10:
                if self.speed > obs['speed_limit']:
                    penalty = 20 if obs['type'] == 'pedestrian' else 10
                    self.score -= penalty
                    self.alerts.append(f"Hit {obs['type']} at {self.speed}km/h!")
                else:
                    self.score += 5
                self.obstacles.remove(obs)
    
    def display_status(self):
        """Show current game state"""
        print(f"📊 Score: {self.score} | 🚗 Speed: {self.speed}km/h | 🛣️ Distance: {self.distance:.0f}m")
        print(f"⏱️ Time: {time.time() - self.start_time:.1f}s")
        
        if self.obstacles:
            next_obs = self.obstacles[0]
            print(f"\n⚠️ Next: {next_obs['type']} in {next_obs['distance'] - self.distance:.0f}m (Limit: {next_obs['speed_limit']}km/h)")
        
        if self.alerts:
            print("\n🚨 Alerts:")
            for alert in self.alerts[-3:]:
                print(f"- {alert}")
    
    def end_game(self):
        """Final results with voice feedback"""
        clear_output()
        duration = time.time() - self.start_time
        
        print("🏁 Game Over! Final Results:")
        print(f"📊 Score: {self.score}/100")
        print(f"🚗 Max Speed: {max(50, self.speed)}km/h")
        print(f"🛣️ Distance: {self.distance:.0f}m")
        print(f"⏱️ Time: {duration:.1f}s")
        
        if self.score >= 80:
            msg = "Excellent driving! You're a pro."
        elif self.score >= 60:
            msg = "Good job, but needs practice."
        else:
            msg = "Needs improvement. Focus on safety."
        
        print(f"\n🔊 {msg}")
        self.text_to_speech(msg)
        
        # Show performance plot
        self.show_performance(duration)
    
    def text_to_speech(self, text):
        """Generate voice feedback"""
        tts = gTTS(text=text, lang='en')
        tts.save("feedback.mp3")
        display(Audio("feedback.mp3"))
    
    def show_performance(self, duration):
        """Create performance visualization"""
        fig, ax = plt.subplots(figsize=(10, 4))
        
        categories = ['Safety', 'Speed', 'Reaction', 'Efficiency']
        
        # Calculate scores with proper parentheses
        speed_score = min(100, max(0, 100 - (max(0, self.speed - 70) * 2))
        reaction_score = min(100, max(0, 100 - len(self.alerts) * 10))
        efficiency_score = min(100, (self.distance/duration) * 2)
        
        values = [self.score, speed_score, reaction_score, efficiency_score]
        
        bars = ax.bar(categories, values, color=['green', 'blue', 'orange', 'purple'])
        ax.set_ylim(0, 110)
        ax.set_title('Driving Performance Breakdown')
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height,
                    f'{int(height)}', ha='center', va='bottom')
        
        plt.show()

# 4. Start the game
game = ADASGame()
game.play()