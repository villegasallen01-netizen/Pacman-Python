import pygame
import math
import sys
import array

# ==========================================
# CONSTANTS & CONFIGURATION
# ==========================================
TILE_SIZE = 24
COLS = 28
ROWS = 31
SCREEN_WIDTH = COLS * TILE_SIZE
SCREEN_HEIGHT = (ROWS + 3) * TILE_SIZE  # Extra space for score display
FPS = 60

# Colors (RGB)
BLACK = (0, 0, 0)
NAVY_BLUE = (0, 33, 165)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
PINK_DOT = (255, 184, 174)
CYAN = (0, 255, 255)
PINK = (255, 184, 255)
ORANGE = (255, 184, 82)
RED = (255, 0, 0)
BLUE_FRIGHTENED = (33, 33, 255)
FLASH_WHITE = (230, 230, 230)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
NONE = (0, 0)

# Classic Pac-Man Maze Grid Layout
# 1 = Wall, 2 = Normal Pellet, 3 = Power Pellet, 0 = Empty/Ghost House
MAZE = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
    [1,3,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,3,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
    [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,2,1,1,1,1,1,0,1,1,0,1,1,1,1,1,2,1,1,1,1,1,1],
    [0,0,0,0,0,1,2,1,1,1,1,1,0,1,1,0,1,1,1,1,1,2,1,0,0,0,0,0],
    [0,0,0,0,0,1,2,1,1,0,0,0,0,0,0,0,0,0,0,1,1,2,1,0,0,0,0,0],
    [0,0,0,0,0,1,2,1,1,0,1,1,1,0,0,1,1,1,0,1,1,2,1,0,0,0,0,0],
    [1,1,1,1,1,1,2,1,1,0,1,0,0,0,0,0,0,1,0,1,1,2,1,1,1,1,1,1],
    [0,0,0,0,0,0,2,0,0,0,1,0,0,0,0,0,0,1,0,0,0,2,0,0,0,0,0,0],
    [1,1,1,1,1,1,2,1,1,0,1,0,0,0,0,0,0,1,0,1,1,2,1,1,1,1,1,1],
    [0,0,0,0,0,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,0,0,0,0,0],
    [0,0,0,0,0,1,2,1,1,0,0,0,0,0,0,0,0,0,0,1,1,2,1,0,0,0,0,0],
    [0,0,0,0,0,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,0,0,0,0,0],
    [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1],
    [1,3,2,2,1,1,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,1,1,2,2,3,1],
    [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
    [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
    [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1],
    [1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

# ==========================================
# RETRO AUDIO SYNTHESIZER (No external files!)
# ==========================================
def generate_tone(frequency, duration, volume=0.3, wave_type='square'):
    """Generates pure retro sound effects on the fly using Pygame sound buffers."""
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    buf = array.array('h', [0] * n_samples)
    amplitude = int(32767 * volume)
    
    for i in range(n_samples):
        t = float(i) / sample_rate
        if wave_type == 'square':
            val = amplitude if math.sin(2 * math.pi * frequency * t) >= 0 else -amplitude
        else:
            val = int(amplitude * math.sin(2 * math.pi * frequency * t))
        buf[i] = val
        
    return pygame.mixer.Sound(buffer=buf)

# Sound caching
SOUNDS = {}

def init_audio():
    pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
    SOUNDS['waka_low'] = generate_tone(240, 0.08, 0.2, 'square')
    SOUNDS['waka_high'] = generate_tone(480, 0.08, 0.2, 'square')
    SOUNDS['power'] = generate_tone(600, 0.25, 0.3, 'square')
    SOUNDS['eat_ghost'] = generate_tone(800, 0.3, 0.4, 'sine')

# ==========================================
# GAME CLASSES
# ==========================================
class PacMan:
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.reset()

    def reset(self):
        self.x = float(self.start_x * TILE_SIZE + TILE_SIZE // 2)
        self.y = float(self.start_y * TILE_SIZE + TILE_SIZE // 2)
        self.dir = NONE
        self.next_dir = NONE
        self.speed = 2.5
        self.mouth_angle = 45
        self.mouth_speed = 4
        self.radius = TILE_SIZE // 2 - 2

    def update(self, grid):
        # Try turning into desired direction if valid
        if self.next_dir != NONE and self.can_move(self.next_dir, grid):
            self.dir = self.next_dir

        # Move if clear ahead
        if self.can_move(self.dir, grid):
            self.x += self.dir[0] * self.speed
            self.y += self.dir[1] * self.speed
            
            # Animate mouth
            self.mouth_angle += self.mouth_speed
            if self.mouth_angle >= 45 or self.mouth_angle <= 0:
                self.mouth_speed *= -1
        else:
            self.mouth_angle = 20

        # Screen Wrap / Warp Tunnels
        if self.x < 0:
            self.x = SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH:
            self.x = 0

    def can_move(self, direction, grid):
        if direction == NONE:
            return False
            
        new_x = self.x + direction[0] * self.speed
        new_y = self.y + direction[1] * self.speed
        
        # Check surrounding tiles
        corners = [
            (new_x - self.radius, new_y - self.radius),
            (new_x + self.radius, new_y - self.radius),
            (new_x - self.radius, new_y + self.radius),
            (new_x + self.radius, new_y + self.radius)
        ]
        
        for cx, cy in corners:
            grid_x = int(cx // TILE_SIZE)
            grid_y = int(cy // TILE_SIZE)
            
            # Allow tunnel warp
            if grid_x < 0 or grid_x >= COLS:
                continue
            if 0 <= grid_y < ROWS:
                if grid[grid_y][grid_x] == 1:
                    return False
        return True

    def draw(self, surface):
        if self.dir == RIGHT:
            start_angle = self.mouth_angle
        elif self.dir == LEFT:
            start_angle = 180 + self.mouth_angle
        elif self.dir == UP:
            start_angle = 90 + self.mouth_angle
        elif self.dir == DOWN:
            start_angle = 270 + self.mouth_angle
        else:
            start_angle = 45

        end_angle = start_angle + (360 - 2 * self.mouth_angle)

        pygame.draw.arc(
            surface, YELLOW,
            (int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2),
            math.radians(start_angle), math.radians(end_angle),
            self.radius
        )


class Ghost:
    def __init__(self, x, y, color):
        self.start_x = x
        self.start_y = y
        self.color = color
        self.reset()

    def reset(self):
        self.x = float(self.start_x * TILE_SIZE + TILE_SIZE // 2)
        self.y = float(self.start_y * TILE_SIZE + TILE_SIZE // 2)
        self.dir = UP
        self.speed = 2.0
        self.frightened = False
        self.frightened_timer = 0
        self.radius = TILE_SIZE // 2 - 2

    def update(self, grid, pacman):
        if self.frightened:
            self.frightened_timer -= 1
            if self.frightened_timer <= 0:
                self.frightened = False

        # Find available directions (no reversing unless stuck)
        valid_dirs = []
        opposite = (-self.dir[0], -self.dir[1])

        for d in [UP, DOWN, LEFT, RIGHT]:
            if d == opposite:
                continue
            if self.can_move(d, grid):
                valid_dirs.append(d)

        if not valid_dirs and self.can_move(opposite, grid):
            valid_dirs.append(opposite)

        if valid_dirs:
            # Ghost AI targeting logic
            if self.frightened:
                # Pick direction that increases distance to Pac-Man
                best_dir = max(valid_dirs, key=lambda d: math.hypot(
                    (self.x + d[0] * TILE_SIZE) - pacman.x,
                    (self.y + d[1] * TILE_SIZE) - pacman.y
                ))
            else:
                # Seek Pac-Man
                best_dir = min(valid_dirs, key=lambda d: math.hypot(
                    (self.x + d[0] * TILE_SIZE) - pacman.x,
                    (self.y + d[1] * TILE_SIZE) - pacman.y
                ))
            self.dir = best_dir

        self.x += self.dir[0] * self.speed
        self.y += self.dir[1] * self.speed

        # Tunnel wrap
        if self.x < 0:
            self.x = SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH:
            self.x = 0

    def can_move(self, direction, grid):
        new_x = self.x + direction[0] * self.speed
        new_y = self.y + direction[1] * self.speed

        grid_x = int(new_x // TILE_SIZE)
        grid_y = int(new_y // TILE_SIZE)

        if grid_x < 0 or grid_x >= COLS:
            return True
        if 0 <= grid_y < ROWS:
            return grid[grid_y][grid_x] != 1
        return False

    def draw(self, surface):
        draw_color = BLUE_FRIGHTENED if self.frightened else self.color
        if self.frightened and self.frightened_timer < 120 and (self.frightened_timer // 15) % 2 == 0:
            draw_color = FLASH_WHITE

        center_x, center_y = int(self.x), int(self.y)
        
        # Dome head & Body
        rect = (center_x - self.radius, center_y - self.radius, self.radius * 2, self.radius * 2)
        pygame.draw.circle(surface, draw_color, (center_x, center_y - 2), self.radius)
        pygame.draw.rect(surface, draw_color, (center_x - self.radius, center_y - 2, self.radius * 2, self.radius))

        # Bottom Skirt Waves
        wave_w = (self.radius * 2) // 3
        for i in range(3):
            wx = center_x - self.radius + i * wave_w + wave_w // 2
            wy = center_y + self.radius - 2
            pygame.draw.circle(surface, draw_color, (wx, wy), wave_w // 2)

        # Eyes
        if not self.frightened:
            eye_offset_x = self.dir[0] * 3
            eye_offset_y = self.dir[1] * 3
            pygame.draw.circle(surface, WHITE, (center_x - 4 + eye_offset_x, center_y - 3 + eye_offset_y), 4)
            pygame.draw.circle(surface, WHITE, (center_x + 4 + eye_offset_x, center_y - 3 + eye_offset_y), 4)
            pygame.draw.circle(surface, BLUE_FRIGHTENED, (center_x - 4 + eye_offset_x, center_y - 3 + eye_offset_y), 2)
            pygame.draw.circle(surface, BLUE_FRIGHTENED, (center_x + 4 + eye_offset_x, center_y - 3 + eye_offset_y), 2)


# ==========================================
# MAIN GAME ENGINE
# ==========================================
class Game:
    def __init__(self):
        pygame.init()
        init_audio()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Classic Pac-Man - Python Retro Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 18, bold=True)
        self.large_font = pygame.font.SysFont("monospace", 32, bold=True)

        self.score = 0
        self.high_score = 0
        self.lives = 3
        self.waka_sound_flip = False

        self.reset_game()

    def reset_game(self):
        self.grid = [row[:] for row in MAZE]
        self.pacman = PacMan(13, 23)
        self.ghosts = [
            Ghost(13, 11, RED),     # Blinky
            Ghost(14, 11, PINK),    # Pinky
            Ghost(13, 14, CYAN),    # Inky
            Ghost(14, 14, ORANGE)   # Clyde
        ]
        self.game_over = False
        self.game_won = False

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.game_over or self.game_won:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.lives = 3
                        self.score = 0
                        self.reset_game()

                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.pacman.next_dir = UP
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.pacman.next_dir = DOWN
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.pacman.next_dir = LEFT
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.pacman.next_dir = RIGHT

    def check_collisions(self):
        grid_x = int(self.pacman.x // TILE_SIZE)
        grid_y = int(self.pacman.y // TILE_SIZE)

        # Eat regular dot
        if 0 <= grid_y < ROWS and 0 <= grid_x < COLS:
            tile = self.grid[grid_y][grid_x]
            if tile == 2:
                self.grid[grid_y][grid_x] = 0
                self.score += 10
                # Play alternate chomping sounds
                if self.waka_sound_flip:
                    SOUNDS['waka_low'].play()
                else:
                    SOUNDS['waka_high'].play()
                self.waka_sound_flip = not self.waka_sound_flip

            # Eat Power Pellet
            elif tile == 3:
                self.grid[grid_y][grid_x] = 0
                self.score += 50
                SOUNDS['power'].play()
                for ghost in self.ghosts:
                    ghost.frightened = True
                    ghost.frightened_timer = 400  # ~6.5 seconds

        # Check Pac-Man vs Ghost collisions
        for ghost in self.ghosts:
            dist = math.hypot(self.pacman.x - ghost.x, self.pacman.y - ghost.y)
            if dist < TILE_SIZE * 0.8:
                if ghost.frightened:
                    SOUNDS['eat_ghost'].play()
                    self.score += 200
                    ghost.reset()
                else:
                    # Life lost
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True
                    else:
                        self.pacman.reset()
                        for g in self.ghosts:
                            g.reset()

        # Check Win Condition (No pellets remaining)
        pellets_remaining = sum(row.count(2) + row.count(3) for row in self.grid)
        if pellets_remaining == 0:
            self.game_won = True

        if self.score > self.high_score:
            self.high_score = self.score

    def render(self):
        self.screen.fill(BLACK)

        # Draw Grid / Maze Walls
        for row in range(ROWS):
            for col in range(COLS):
                val = self.grid[row][col]
                x = col * TILE_SIZE
                y = row * TILE_SIZE

                if val == 1:
                    pygame.draw.rect(self.screen, NAVY_BLUE, (x, y, TILE_SIZE, TILE_SIZE), 2, border_radius=4)
                elif val == 2:
                    pygame.draw.circle(self.screen, PINK_DOT, (x + TILE_SIZE // 2, y + TILE_SIZE // 2), 3)
                elif val == 3:
                    # Pulsing power pellet effect
                    radius = 6 + int(math.sin(pygame.time.get_ticks() * 0.01) * 2)
                    pygame.draw.circle(self.screen, PINK_DOT, (x + TILE_SIZE // 2, y + TILE_SIZE // 2), radius)

        # Draw Entities
        self.pacman.draw(self.screen)
        for ghost in self.ghosts:
            ghost.draw(self.screen)

        # Draw UI / HUD
        hud_top = ROWS * TILE_SIZE + 10
        score_text = self.font.render(f"SCORE: {self.score}", True, WHITE)
        high_score_text = self.font.render(f"HIGH: {self.high_score}", True, WHITE)
        self.screen.blit(score_text, (20, hud_top))
        self.screen.blit(high_score_text, (SCREEN_WIDTH - 160, hud_top))

        # Draw Lives (Pacman Icons)
        for i in range(self.lives):
            lx = 20 + i * 25
            ly = hud_top + 30
            pygame.draw.circle(self.screen, YELLOW, (lx, ly), 9)

        # Draw Overlay Messaging
        if self.game_over:
            msg = self.large_font.render("GAME OVER", True, RED)
            sub = self.font.render("PRESS ENTER TO RESTART", True, WHITE)
            self.screen.blit(msg, (SCREEN_WIDTH // 2 - 85, SCREEN_HEIGHT // 2 - 20))
            self.screen.blit(sub, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 20))
        elif self.game_won:
            msg = self.large_font.render("YOU WIN!", True, YELLOW)
            sub = self.font.render("PRESS ENTER TO RESTART", True, WHITE)
            self.screen.blit(msg, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 20))
            self.screen.blit(sub, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 20))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            
            if not self.game_over and not self.game_won:
                self.pacman.update(self.grid)
                for ghost in self.ghosts:
                    ghost.update(self.grid, self.pacman)
                self.check_collisions()

            self.render()
            self.clock.tick(FPS)

# ==========================================
# ENTRY POINT
# ==========================================
if __name__ == "__main__":
    game = Game()
    game.run()