import pygame
import os

pygame.init()

screen_width = 1000
screen_height = 500 
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ethan Pang")

clock = pygame.time.Clock() 

current_path = os.path.dirname(__file__)
images_path = os.path.join(current_path, "images")

# 이미지 불러오기 
# 배경 
background = pygame.image.load(os.path.join(images_path, "background.png"))

# 스테이지
stage = pygame.image.load(os.path.join(images_path, "stage.png"))
stage_size = stage.get_rect().size 
stage_height = stage_size[1]

# 캐릭터 
character = pygame.image.load(os.path.join(images_path, "character.png"))
character_size = character.get_rect().size 
cahracter_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (cahracter_width/ 2)
character_y_pos = screen_height - stage_height - character_height

# 캐릭터를 더 정확히 이동시키기 위해서 ex. 오른쪽 버튼 누름 -> 왼쪽 버튼 누름 -> 오른쪽 버튼을 뗌 => 캐릭터 움직이지 않음 (맨 마지막에 일어난 이벤트가 KEYUP 이기 때문)
character_to_left_x = 0
character_to_right_x = 0 
character_to_y = 0
character_speed = 1
character_jump_speed = 0.5

# 아래 방향키를 눌렀을 때, 찌부되는 캐릭터 
down_character = pygame.image.load(os.path.join(images_path, "down_character.png"))
down_character_size = down_character.get_rect().size 
down_character_width = down_character_size[0]
down_character_height = down_character_size[1]
down_character_y_pos = screen_height - stage_height - down_character_height 

# 무기 
weapons = [] 
weapon_speed = 0.5

weapon = pygame.image.load(os.path.join(images_path, "weapon.png"))
weapon_size = weapon.get_rect().size 
weapon_width = weapon_size[0]
weapon_height = weapon_size[1]

# 볼 
balls = []
ball_init_y_speed = [-18, -15, -12, -9]
ball_images = [pygame.image.load(os.path.join(images_path, "balloon{}.png".format(i))) for i in range(1, 5)] 
ball_sizes = [ball_images[i].get_rect().size[0] for i in range(4)]
# 게임 시작 시, 초기 화면에서 큰 공 하나 나타남 
balls.append({
    "x_pos" : 50,
    "y_pos" : screen_height - stage_height - ball_sizes[0],
    "img_idx" : 0,
    "to_x" : 3,
    "to_y" : ball_init_y_speed[0]
})

total_time = 100 
game_font = pygame.font.Font(None, 40) # 기본 폰트 사용, 폰트 사이즈 40 
start_ticks = pygame.time.get_ticks() 

game_result = "Game Over" # 기본값, 볼과 캐릭터가 부딪혔을 때 

running = True 
weapon_running = False 
weapon_times = 0 # 연속발사 횟수 제한 
jump_limit = 150 

while running:
    dt = clock.tick(60)

    for event in pygame.event.get(): # 이벤트(키보드 누르기, 떼기, 창닫기 등)가 일어났을 떄만 실행 
        if event.type == pygame.QUIT:
            running = False
        
        # 캐릭터 이동 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_left_x -= character_speed
            if event.key == pygame.K_RIGHT:
                character_to_right_x += character_speed
            # 무기 발사  
            if event.key == pygame.K_SPACE:
                weapon_running = True # 스페이스바를 떼지 않는 이상 계속 True 
            # 캐릭터 점프
            if event.key == pygame.K_UP:
                character_to_y -= character_jump_speed
            # 캐릭터 찌부 
            if event.key == pygame.K_DOWN:
                character = down_character
                cahracter_width = down_character_width
                character_height = down_character_height
                character_y_pos = down_character_y_pos
                   
        if event.type == pygame.KEYUP: 
            if event.key == pygame.K_LEFT:
                character_to_left_x = 0 
            if event.key == pygame.K_RIGHT:
                character_to_right_x = 0 
            if event.key == pygame.K_SPACE:
                weapon_times = 0   
                weapon_running = False # 스페이스바에서 손을 떼는 순간 아래 if문 실행 중단 -> 더 이상 무기 생성 안함 
            if event.key == pygame.K_DOWN:
                character = pygame.image.load(os.path.join(images_path, "character.png"))
                cahracter_width = character_size[0]
                character_height = character_size[1]
                character_y_pos = down_character_y_pos - (character_height - down_character_height)

    # 캐릭터의 x 좌표 업데이트 
    character_x_pos += (character_to_left_x + character_to_right_x) *dt 
    character_y_pos += character_to_y * dt 

    # 캐릭터의 경계값 설정 
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - cahracter_width: 
        character_x_pos = screen_width - cahracter_width 

    # 캐릭터 점프 시, 경계값 설정 (jump_limit 정도만 위로 올라갔다가, 알아서 다시 땅으로 착지)
    if character_y_pos < screen_height - stage_height - character_height - jump_limit:
        character_to_y = 0 # 0으로 초기화 후 
        character_to_y += character_jump_speed # 아래 방향으로 이동하도록 조정 
    elif character_y_pos > screen_height - stage_height - character_height:
        character_y_pos = screen_height - stage_height - character_height
        character_to_y = 0 

    # 무기 연속 발사 
    if weapon_running:
        if weapon_times < 10:
            weapon_x_pos = character_x_pos + (cahracter_width / 2) - (weapon_width / 2)
            weapon_y_pos = character_y_pos
            weapons.append([weapon_x_pos, weapon_y_pos])
            weapon_times += 1
        else:
            weapon_times = 0   
            weapon_running = False # 무기 발사 10회 하면 연속 발사 불가능 -> 다시 스페이스바를 눌러야 함            

    # 무기 발사 후, 위로 이동 
    for weapon_idx, weapon_val in enumerate(weapons):
        weapon_val[1] -= weapon_speed * dt 
        if weapon_val[1] < -weapon_height: # 무기가 천장에 닿으면
            del weapons[weapon_idx] # 삭제 

    # 볼의 이동
    # x 축 방향
    for ball_idx, ball_val in enumerate(balls):
        ball_val["x_pos"] += ball_val["to_x"]
        ball_val["y_pos"] += ball_val["to_y"] 

        # 볼에 대한 정보 
        ball_x_pos = ball_val["x_pos"]
        ball_y_pos = ball_val["y_pos"]
        ball_img_idx = ball_val["img_idx"]
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_width = ball_rect.size[0]
        ball_height = ball_rect.size[1]

        if ball_x_pos < 0 or ball_x_pos > screen_width - ball_width: # 볼이 벽에 부딪히면 
            ball_val["to_x"] *= -1 # 반대 방향으로 이동 
        if ball_y_pos > screen_height - stage_height - ball_height: # 복이 바닥에 닿으면 
            ball_val["to_y"] = ball_init_y_speed[ball_img_idx] # 초기 y 이동 속도로 변환 
        
        ball_val["to_y"] += 0.3 # y축 이동 거리가 점점 짧아졌다가 다시 늘어남   

        # 볼 - 캐릭터 충돌 처리 
        ball_rect.left = ball_x_pos
        ball_rect.top = ball_y_pos

        character_rect = character.get_rect()
        character_rect.left = character_x_pos
        character_rect.top = character_y_pos

        if ball_rect.colliderect(character_rect): 
            running = False
            break

        # 볼 - 무기 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_val[0] 
            weapon_rect.top = weapon_val[1]

            # 충돌하면 공이 쪼개짐 -> 서로 충돌한 무기와 공을 바로 제거 
            # -> 그렇지 않고 인덱스 번호로 제거할 무기와 공을 받으면, 남아 있는 무기가 다른 공과 다시 충돌, 그 충돌한 공이 다시 인덱스 번호로 넘겨짐
            # => 처음 충돌한 공은 살아남고, 쪼개져 생성된 공이 사라짐 
            # 해결법 
            # 1) 충돌 시, 공과 무기를 바로 없앰 -> 선택 
            # 2) 충돌한 후 내부 for문과 외부 for문을 모두 빠져나오도록 설정  
            if ball_rect.colliderect(weapon_rect): 
                del balls[ball_idx] # 충돌한 볼 삭제 
                del weapons[weapon_idx] # 충돌한 무기 삭제 
                
                # 크기가 더 작은 공 2개 생성 (3번째 공까지만 가능) 
                if ball_img_idx < 3:
                    small_ball_size = ball_images[ball_img_idx + 1].get_rect().size
                    small_ball_width = small_ball_size[0]
                    small_ball_height = small_ball_size[1]

                    # 공의 x축 진행방향 중요 -> 하나는 왼쪽, 하나는 오른쪽 
                    balls.append({
                        "x_pos" : ball_x_pos + (ball_width / 2) - (small_ball_width / 2),
                        "y_pos" : ball_y_pos + (ball_height / 2) - (small_ball_height / 2), 
                        "img_idx" : ball_img_idx + 1,
                        "to_x" : -3,
                        "to_y" : ball_init_y_speed[ball_img_idx + 1]
                    })

                    balls.append({
                        "x_pos" : ball_x_pos + (ball_width / 2) - (small_ball_width / 2),
                        "y_pos" : ball_y_pos + (ball_height / 2) - (small_ball_height / 2), 
                        "img_idx" : ball_img_idx + 1,
                        "to_x" : 3,
                        "to_y" : ball_init_y_speed[ball_img_idx + 1]
                    })

                break 

# ========================================================================================
# 화면에 그리기 
    screen.blit(background, (0, 0))

    for w in weapons:
        screen.blit(weapon, (w[0], w[1]))

    for ball_val in balls:
        ball_x_pos = ball_val["x_pos"]
        ball_y_pos = ball_val["y_pos"]
        ball_img_idx = ball_val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_x_pos, ball_y_pos))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos)) 

    elapsed_ticks = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_ticks)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    pygame.display.update()

    if total_time - elapsed_ticks <= 0:
        game_result = "Time Over"
        running = False 

    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False 

# 게임 결과 보여주기 
msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center=(screen_width / 2, screen_height / 2))
screen.blit(msg, msg_rect)
pygame.display.update() 
pygame.time.delay(2000) # 2초 딜레이 (2초간 화면 정지)

pygame.quit()     
