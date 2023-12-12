import pygame
import random
import os

class StartScreen:
    def __init__(self, screen):
        self.screen = screen
        self.start_button = pygame.image.load(os.path.join(image_path, "pizza.png"))
        self.start_button_rect = self.start_button.get_rect(center=(screen_width // 2, screen_height // 2))
        self.background = pygame.image.load(os.path.join(image_path, "bg.jpg"))
        self.font = pygame.font.Font("assets/shroomsgarden.ttf", 50)
        self.title_text = self.font.render("Pyzza! Press the Pizza to start", True, (255, 255, 255))

    def draw(self, screen):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.start_button, self.start_button_rect)
        self.screen.blit(self.title_text, (screen_width // 2 - self.title_text.get_width() // 2, 50))

class Player(pygame.sprite.Sprite):
    def __init__(self, images, size, speed, initial_x, initial_y):
        super().__init__()
        self.images = [pygame.transform.scale(image, size) for image in images]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = initial_x
        self.rect.y = initial_y
        self.speed = speed
        self.crash_effect = CrashEffect(self.rect.x, self.rect.y)
        self.crash_effects = pygame.sprite.Group()
        self.frame = 0
        self.animation_speed = 10 # 애니메이션 속도 조절

    def update(self,current_life, lives, obstacles, crash_effects):
        keys = pygame.key.get_pressed()

        # 애니메이션 업데이트
        if self.frame % self.animation_speed == 0:
            self.image = self.images[self.frame // self.animation_speed]
            self.frame = (self.frame + 1) % (len(self.images) * self.animation_speed)

        # 플레이어 위아래로 이동
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # 화면 범위 제한
        if self.rect.y < 100:
            self.rect.y = 100
        elif self.rect.y > screen_height - self.rect.height:
            self.rect.y = screen_height - self.rect.height

        # 현재 목숨에 따라 플레이어 이미지 업데이트
        if current_life > 0:
            self.update_images(current_life)

    def update_images(self, current_life):
        self.images = [pygame.image.load(os.path.join(image_path, f"player_{i}.png")) for i in range(current_life, 0, -1)]
        self.image = self.images[0]

    def handle_collision(self, group, crash_effects):
        # 플레이어와 그룹의 스프라이트 간의 충돌을 처리합니다.
        collisions = pygame.sprite.spritecollide(self, group, True)
        for sprite in collisions:
            crash_effect = CrashEffect(self.rect.x, self.rect.y)
            crash_effects.add(crash_effect)
            crash_effect.play()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, size, speed, obstacle_type):
        super().__init__()
        self.image = pygame.transform.scale(image, size)
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.rect.y = random.randint(0, screen_height - size[1])
        self.speed = speed
        self.obstacle_type = obstacle_type

    def update(self):
        self.rect.x -= self.speed
        if self.rect.y < 100:
            self.rect.y = 100
        elif self.rect.y > screen_height - self.rect.height:
            self.rect.y = screen_height - self.rect.height

class Life(pygame.sprite.Sprite):
    def __init__(self, image_path, initial_x, initial_y):
        super().__init__()
        self.original_image = pygame.image.load(image_path)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = initial_x
        self.rect.y = initial_y

    def update(self, current_life):
        if current_life > 0:
            self.rect.x = 10
        else:
            self.rect.x = -1000

class CrashEffect(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load(os.path.join(image_path, "angry.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 
        self.frame = 0
        self.animation_speed = 10  # 애니메이션 속도 조절
        self.sound = pygame.mixer.Sound(os.path.join(current_path, "assets/sound/crash.mp3"))

    def update(self):
        # 애니메이션 업데이트
        if self.frame % self.animation_speed == 0:
            self.image = pygame.image.load(os.path.join(image_path, f"angry.png"))
            self.frame = (self.frame + 1) % (len(self.image) * self.animation_speed)

        # 사운드 재생
        self.sound.play()

        # 다 재생되면 제거
        if self.frame == len(self.images) * self.animation_speed - 1:
            self.kill()

class SuccessScreen:
    def __init__(self, screen):
        self.screen = screen
        self.smile_image = pygame.image.load(os.path.join(image_path, "smile.png"))
        self.smile_rect = self.smile_image.get_rect(center=(screen_width // 2, screen_height // 2))
        self.font = pygame.font.Font("assets/shroomsgarden.ttf", 50)
        self.success_text = self.font.render("Success!", True, (255, 255, 255))
        self.success_rect = self.success_text.get_rect(center=(screen_width // 2, screen_height // 2 + 200))

    def draw(self):
        self.screen.blit(self.smile_image, self.smile_rect)
        self.screen.blit(self.success_text, self.success_rect)

# 화면 설정
screen_width = 1123
screen_height = 632
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pyzza!")
initial_life_x = 10
initial_life_y = 10
current_life = 3

# 이미지 경로
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "assets")
image_in_path = os.path.join(current_path, "assets/in")
image_no_path = os.path.join(current_path, "assets/no")
background = pygame.image.load(os.path.join(image_path, "bg.jpg"))

def start_screen():
    start_screen = StartScreen(screen)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_screen.start_button_rect.collidepoint(event.pos):
                    return

        start_screen.draw(screen)
        pygame.display.flip()
        clock.tick(30)

def main():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    custom_font = pygame.font.Font("assets/shroomsgarden.ttf", 50)

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pyzza!")

    running = True
    success = False
    end_image_index = 0
    game_started = False
    score = 0
    goal_score = 400
    current_life = 3
    initial_life_x = 10

    success_screen = SuccessScreen(screen)
    success_effect = None
    crash_effects = pygame.sprite.Group()
    start_screen()

    # 플레이어 설정
    player_images = [pygame.image.load(os.path.join(image_path, f"player_{i}.png")) for i in range(current_life, 0, -1)]
    player = Player(player_images,(100,100),20,100,550)

    # 목숨 이미지
    life_images = [pygame.image.load(os.path.join(image_path, f"life_{i}.png")) for i in range(1,4)]
    lives = pygame.sprite.Group()
    for i in range(current_life,0,-1):
        life = Life(os.path.join(image_path, f"life_{i}.png"), initial_life_x, initial_life_y)
        lives.add(life)
        initial_life_x += life.rect.width + 5

    # 장애물 설정
    obstacle_size = (100, 100)
    obstacle_speed = 25
    obstacle_images = {
        "bonus": [pygame.image.load(os.path.join(image_in_path, file)) for file in os.listdir(image_in_path)],
        "no": [pygame.image.load(os.path.join(image_no_path, file)) for file in os.listdir(image_no_path)],
    }
    obstacles = pygame.sprite.Group()

    while running == True and score >= 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_started:
            start_screen()
            game_started = True
        
        while player.rect.x < screen_width and score < goal_score:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.blit(background, (0, 0))
            player.update(current_life,lives, obstacles, crash_effects)
        
            # 장애물 생성
            if random.randint(1, 100) < 5:
                obstacle_type = random.choice(["bonus", "no"])
                obstacle = Obstacle(random.choice(obstacle_images[obstacle_type]), obstacle_size, obstacle_speed, obstacle_type)
                obstacles.add(obstacle)
            
            obstacles.update()

            # 플레이어와 장애물 충돌 체크
            collisions = pygame.sprite.spritecollide(player, obstacles, True)
            for obstacle in collisions:
                if obstacle.obstacle_type == "bonus":
                    score += 40
                elif obstacle.obstacle_type == "no":
                    current_life -= 1
                    if current_life > 0:
                        if lives.sprites():    
                            lives.remove(lives.sprites()[0]) 
                    crash_effect = CrashEffect(player.rect.x, player.rect.y)
                    crash_effects.add(crash_effect)
                if current_life == 0:
                    running = False
                        
            lives.update(current_life)
            lives.draw(screen)
            screen.blit(player.image, player.rect)

            # 장애물 이미지 설정
            for obstacle in obstacles:
                screen.blit(obstacle.image, obstacle.rect)

            # 점수 표시
            score_text = custom_font.render("Score: {}".format(score), True, (255, 255, 255))
            screen.blit(score_text, [screen_width - score_text.get_width() - 10, 10])

            # 목표 달성 시 게임 종료 이미지 표시
            if score >= goal_score:
                end_image = pygame.image.load(os.path.join(image_path,"smile.png"))
                screen.blit(pygame.transform.scale(end_image, (screen_width, screen_height)), (0, 0))
                pygame.display.flip()
                pygame.time.delay(2000)  # 2초 대기
                running = False

            pygame.display.flip()

            # 초당 프레임 설정
            pygame.time.Clock().tick(30)

    # 게임 종료
    pygame.quit()

if __name__ == "__main__":
    main()