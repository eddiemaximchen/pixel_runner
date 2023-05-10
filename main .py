import pygame,sys
from random import randint
def display_score(): #顯示積分
    current_time = int(pygame.time.get_ticks()/1000)-start_time #把毫秒轉成秒
    score_surf=test_font.render(f'Score: {current_time}',True,(64,64,64)) #true表平滑化 否則 s 太像 8
    score_rect=score_surf.get_rect(center=(400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    #表示obstacle_list 有值
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            #速度
            obstacle_rect.x -= 5
            #兩種敵人最大的差異飛行高度
            if obstacle_rect.bottom ==300:
                screen.blit(snail_surf,obstacle_rect)
            else:
                screen.blit(fly_surf,obstacle_rect)
        obstacle_list=[obstacle for obstacle in obstacle_list if obstacle.x>-100] #只把符合條件的 obstacle 加入 list
        return obstacle_list
    else:
        return [] #沒東西會變None object 所以要回傳空集合
    
def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                #一相撞就return false
                return False
    return True

def player_animation():
    #display walking animation when the player is on the floor
    #display jump image when the player is not on the floor
    global player_surf,player_index
    #表示在空中
    if player_rect.bottom <300:
        player_surf=player_jump
    else :
        #player_index值越大 player看起來跑越快
        player_index += 0.1 
        #0,1交替
        if player_index>=len(player_walk):
            player_index=0
        player_surf=player_walk[int(player_index)]
pygame.init()
screen=pygame.display.set_mode((800,400))#做出視窗 高度不包括視窗列
pygame.display.set_caption('my_game') #設定視窗標題
clock=pygame.time.Clock() #啟動計時器
#放文字方塊 方法：create a font first and create a surface and put the text in that surface
test_font=pygame.font.Font('font/Pixeltype.ttf',50) #第一個參數是font type 第二個參數是 font size
# score_surf=test_font.render('My game',False,'Black') #第二個參數表是否平滑化
score_surf=test_font.render('My game',False,(64,64,64))  #使用自訂顏色
score_rect=score_surf.get_rect(center=(400,50))
#放圖片 每張圖都是一個surface  image要convert
sky_surface=pygame.image.load('graphics/Sky.png').convert() 
ground_surface=pygame.image.load('graphics/ground.png').convert()
#敵人設定 (兩種敵人) 動畫設定
#timer 功能就像 JS setTimeInterval()
obstacle_timer=pygame.USEREVENT +1 #建立一個 event listener +1是因為有些值在pygame.init()就已經不是 0 了
pygame.time.set_timer(obstacle_timer,1500) #建立timer 每1500毫秒啟動一次,製造敵人
snail_animation_timer=pygame.USEREVENT+2 #控制snail animateion
pygame.time.set_timer(snail_animation_timer,500)
fly_animation_timer=pygame.USEREVENT+3   #控制fly animateion
pygame.time.set_timer(fly_animation_timer,200)
snail_frame_1=pygame.image.load('graphics/snail/snail1.png').convert_alpha() #讓背景透明
snail_frame_2=pygame.image.load('graphics/snail/snail2.png').convert_alpha() 
# snail_rect=snail_surf.get_rect(bottomright=(600,300))
snail_frames=[snail_frame_1,snail_frame_2]
snail_frame_index=0
snail_surf=snail_frames[snail_frame_index]
snail_rect=snail_surf.get_rect


fly_frame_1=pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2=pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames=[fly_frame_1,fly_frame_2]
fly_frame_index=0
fly_surf=fly_frames[fly_frame_index]


obstacle_rect_list=[]

#玩家設定 動畫設定
player_walk_1=pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2=pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_index=0
player_walk=[player_walk_1,player_walk_2]
player_jump=pygame.image.load('graphics/player/jump.png').convert_alpha()
player_surf=player_walk[player_index]
player_rect=player_surf.get_rect(midbottom=(80,300)) #紀錄角色的長寬 大小 surface的起點永遠是左上  rect可以是任何點
player_jump_sound=pygame.mixer.Sound('audio/jump.mp3')
player_jump_sound.set_volume(0.5) #設定音量

#game value init
player_gravity=0
start_time=0
score=0
bg_Music=pygame.mixer.Sound('audio/music.wav')
bg_Music.play(loops=-1) #-1表永遠重複
#intro screen
player_stand=pygame.image.load('graphics/player/player_stand.png').convert_alpha()
# player_stand=pygame.transform.scale(player_stand,(200,400)) #傳入一個surface 然後需要多大 回傳一個surface 可以覆蓋自己
# player_stand=pygame.transform.scale2x(player_stand) #直接變兩倍大
player_stand=pygame.transform.rotozoom(player_stand,0,2) # 角度跟倍數
player_stand_rect=player_stand.get_rect(center=(400,200))
game_name=test_font.render('Pixel Runner',False,(111,196,1))
game_name_rect=game_name.get_rect(center=(400,80))

game_message=test_font.render("Press space to play",True,(111,196,1))
game_message_rect=game_message.get_rect(center=(400,340))
game_active=False
#放色塊
# text_font=pygame.font.Font(None,50)
# text_surface=text_font.render('score',False,'Black')
# text_surface.fill('Red') #把test_surface塗成紅色  fill會整塊變黑色 不會達成背景色效果
# text_rect=text_surface.get_rect(topleft=(0,0))


while True:
    #draw all elements
    #update everything
    #按x可以關掉視窗
    for event in pygame.event.get(): #攔截所有event, pygame.QUIT就是點擊x按鈕

        # if event.type==pygame.MOUSEBUTTONUP:
            # pass
        #初始化遊戲
        #在event裡找mouse event,移動滑鼠時才能得到位置 collidepoint 表滑鼠點到人
        if game_active:
            if event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                if player_rect.collidepoint(mouse_pos):
                    player_gravity = -20
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom>=300:
                    player_gravity= -20 
                    player_jump_sound.play()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active=True
                # snail_rect.left=800
                start_time=int(pygame.time.get_ticks()/1000)

        #如果遊戲進行中 每900毫秒要做的事
        if game_active:
            if event.type ==obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright=(randint(900,1100),300))) #敵人會出現的位置
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900,1100),210)))
            
            #控制敵人動畫用
            if event.type==snail_animation_timer:
                if snail_frame_index==0:
                    snail_frame_index=1
                else:
                    snail_frame_index=0
                snail_surf=snail_frames[snail_frame_index]
            
            if event.type==fly_animation_timer:
                if fly_frame_index==0:
                    fly_frame_index=1
            else:
                fly_frame_index=0
            fly_surf=fly_frames[fly_frame_index]


        if event.type==pygame.QUIT:
            pygame.quit() # pygame.quit就像return一樣 下面的pygame code都不會執行
            sys.exit() #脫離while loop  
    if game_active==True:
        #keyboard input 也是分pygame.key, eventloop
        #surface display surface--make things visible. must be unique
        #surface--show a single image and need to attach to display surface. can have many instance
        # screen.blit(ground_surface,(0,0)) # sky is bigger than ground. therefore if sky is not the first image, it will cover all other images
        screen.blit(sky_surface,(0,0)) # blit就是把surface 放到 display surface 上#位置從左上角起算 向右加x 向下加y
        screen.blit(ground_surface,(0,300))
        #紀錄玩家分數
        score=display_score()
        # pygame.draw.rect(screen,'#c0e8ec',score_rect)
        # pygame.draw.rect(screen,'#c0e8ec',score_rect,10)
        # pygame.draw.line(screen,'Gold',(0,0),pygame.mouse.get_pos(),10)
        # pygame.draw.ellipse(screen,'Brown',pygame.Rect(50,200,100,100)) #畫一個圓形 四個參數分別為左 上 寬  高
        # pygame.draw.rect(screen,'Pink',score_rect,6,20) #6是邊框厚度  20是圓腳弧度
        # screen.blit(score_surf,score_rect)

        #player
        player_gravity += 1
        player_rect.y += player_gravity #player向下
        if player_rect.bottom >=300:
            player_rect.bottom=300      #因為底圖的y就是300
        player_animation()
        # screen.blit(player_surf,(80,200)) 用下面的player_rect取代了
        screen.blit(player_surf,player_rect)
        #900毫秒觸發敵人狀況 然後送進 obstacle_movement 設定速度 然後回傳
        # 一定要放在game loop裡
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        #多個敵人的相撞事件
        game_active=collisions(player_rect,obstacle_rect_list)
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
            # print('jump')
        # screen.blit(text_surface,text_rect)
        # snail_x_pos -=4 #每個frame都移動四個單位
        #超出邊界就重設
        # if snail_x_pos==0:  surface的設法
            # snail_x_pos=800
        #沒放背景就直接動畫 會出現殘像 因為沒有背景把之前的snail蓋掉
    
        # 單一隻怪物的運行程式
        # screen.blit(snail_surf,snail_rect)
        # snail_rect.x -= 4
        # if snail_rect.right<=0:snail_rect.left=800
    
        # if player_rect.colliderect(snail_rect): #有相撞的到1 沒相撞得到0 會發生多次
        

        #得到滑鼠事件  pygame.mouse event loop if event type=mouse....
        # mouse_pos=pygame.mouse.get_pos()
        # if player_rect.collidepoint(mouse_pos): #滑鼠是否碰到player
            # print(pygame.mouse.get_pressed())  #return 三個值 分別為左中右滑鼠按鍵是否按下


        #玩家碰到蝸牛要掛掉 但是不退出遊戲
        mouse_pos=pygame.mouse.get_pos()
        # if snail_rect.colliderect(player_rect):
        # game_active=False
    else:
        screen.fill((94,129,162))#只是改顏色
        screen.blit(player_stand,player_stand_rect)
        score_message=test_font.render(f'Your score:{score}',True,(116,196,169))
        score_message_rect=score_message.get_rect(center=(400,330))
        screen.blit(game_name,game_name_rect)
        #結束時清空list 即返回初始值
        obstacle_rect_list.clear()
        player_rect.midbottom=(80,300)
        player_gravity=0
        if score == 0:
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)
    #讓視窗維持出現
    pygame.display.update()
    clock.tick(60) # the true loop can not run faster than 60 times per sec