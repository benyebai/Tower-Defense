# a tower defence game based on direction selection and special moves on different units. You place units to defend against waves of enemies
# written by: Ben

import simplegui
import math
import random
import time

frames_passed = 0
hp = 3
currency = 0
delta_time = 0
previous_time = time.time()
canvas_copy = None

game_screen = 'menu'

WIDTH = 1200 
HEIGHT = 950

# for selection states, and letting the code know, wut step of the placement process the player is at
state = 'select'
character_selected = ''
info_selected = None
pseudo_place = None

# list of everything on field
placed_units = []
enemies_spawned = []

#used for seeing whos on the field
placed_units_names = []

# 'nero', 'ishtar', 'mashu', 'fox', 'healer'
squad = []


Sbutton = None
Rbutton = None
# menu buttons
selection = None
journal = None
controls = None

# stage selection
stage1 = None
stage2 = None
stage3 = None

# pause menu buttons
menu = None
stage_selection = None

# end lvl buttons
stage = None
menu2 = None

current_music = 'menu'
music = {
            'stage1': simplegui.load_sound('https://vgmsite.com/soundtracks/nier-automata-original-soundtrack/wbcxjbpx/1-02%20City%20of%20Ruins%20-%20Rays%20of%20Light.mp3'),
            'stage2': simplegui.load_sound('https://vgmsite.com/soundtracks/nier-automata-original-soundtrack/iclchkkb/1-04%20Memories%20of%20Dust.mp3'),
            'stage3': simplegui.load_sound('https://vgmsite.com/soundtracks/nier-automata-original-soundtrack/fcuncwqu/1-08%20A%20Beautiful%20Song.mp3'),
            'menu': simplegui.load_sound('https://vgmsite.com/soundtracks/nier-automata-original-soundtrack/sqvubkiu/2-15%20Weight%20of%20the%20World.mp3')


}

# pictures for the 2 buttons next to the character info screen
retreat = simplegui.load_image('https://imgur.com/ko0vthW.png')
special = simplegui.load_image('https://imgur.com/NLkt6LB.png')

# set lvls and trails and enemy spawns
stages = {
            'stage1': {		
                            'image': simplegui.load_image('https://imgur.com/R2nt83K.png'),
                            'trail': [[0, 250], [350, 250], [350, 450], [1150, 450]],
                            'spawn': [['bug', 100], ['bug', 600], ['bug', 900], ['bug', 1400], ['spider', 1700], ['bug', 2000], ['spider', 2400], ['bug', 2800], ['bug', 3400],
                                      ['bug', 4000], ['bug', 4100], ['spider', 4150], ['bug', 4200], ['bug', 5000] ,['spider', 5050], ['bug', 5100], ['spider', 5150], ['bug', 5200],
                                      ['spider', 5250], ['spider', 5280], ['spider', 5320]]
                      },	
                
            'stage2': {
                            'image': simplegui.load_image('https://imgur.com/FnH1MsK.png'),
                            'trail': [[0, 150], [350, 150], [350, 650], [650, 650], [650, 350], [1200, 350]],
                            'spawn': [['bug', 200], ['fly', 1050], ['bug', 1500], ['fly', 2200], ['bug', 2500], ['spider', 2700], ['fly', 3000], ['laser', 3500],
                                      ['bug', 3800], ['bug', 4100], ['fly', 4400], ['kamikaze', 4500], ['fly', 4700], ['bug', 4900], ['laser', 5100], ['fly', 5200],
                                      ['fly', 5300], ['fly', 5400], ['kamikaze', 5450], ['kamikaze', 5600], ['laser', 5700], ['laser', 5780], ['fly', 5800]]
                      },	
    
            'stage3': {
                            'image': simplegui.load_image('https://imgur.com/sPBLLdr.png'),
                            'trail': [[150, 0], [150, 350], [350, 350], [350, 150], [550, 150], [550, 650], [950, 650], [950, 250], [1200, 250]],
                            'spawn': [['bug', 200], ['fly', 500], ['spider', 850], ['caster', 1300], ['bug', 2000], ['bug', 2060], ['spider', 2120], ['fly', 2200], ['kamikaze', 2800],
                                      ['caster', 3500], ['laser', 3600], ['knight', 3700], ['spider', 3750], ['kamikaze', 3850], ['bug', 3900], ['caster', 5000], ['caster', 5100],
                                      ['radiance', 5150], ['knight', 5200], ['knight', 5250], ['kamikaze', 5300], ['kamikaze', 5350], ['fly', 5400], ['laser', 5500], 
                                      ['knight', 6000], ['caster', 6050], ['kamikaze', 6100], ['kamikaze', 6120], ['kamikaze', 6140], ['fly', 6200], ['laser', 6250], ['fly', 6300], ['kamikaze', 6320], 
                                      ['kamikaze', 6350], ['knight', 6400]]
                      }	
    
    
         }

# used for figuring which stage is selected and the enemy count
currentlvl = None
currentlvl_left = None

enemies_info = {
    
                'bug': {
                            'img': simplegui.load_image('https://imgur.com/oHfBPdq.png'),
                            'info': [110, 83],
                            'size': [55, 41.5]
                       },
                
                'fly': {
                            'img': simplegui.load_image('https://imgur.com/BXU7AwU.png'),
                            'info': [124, 200],
                            'size': [62, 100]
                       },
                
                'spider': {
                            'img': simplegui.load_image('https://imgur.com/nvswHO4.png'),
                            'info': [130, 91],
                            'size': [65, 45.5]
                       },
                
                'laser': {
                            'img': simplegui.load_image('https://imgur.com/npLNtr0.png'),
                            'info': [250, 274],
                            'size': [100, 124]
                       },
                
                'caster': {
                            'img': simplegui.load_image('https://imgur.com/U0RLtRp.png'),
                            'info': [98, 193],
                            'size': [49, 96]
                       },
                
                'kamikaze': {
                            'img': simplegui.load_image('https://imgur.com/98dPXJ7.png'),
                            'info': [475, 289],
                            'size': [75, 37.8]
                       },
    
                'radiance': {
                            'img': simplegui.load_image('https://imgur.com/bduE2rf.png'),
                            'info': [310, 450],
                            'size': [290, 430]
                       },
    
                'knight': {
                            'img': simplegui.load_image('https://imgur.com/BcmxYpU.png'),
                            'info': [369, 394],
                            'size': [123, 131.3]
                       }
               
               
               
               
               }

units_info = {
               'nero': {
                        'img': simplegui.load_image('https://imgur.com/RQhqLuC.png'),
                        'special': simplegui.load_image('https://imgur.com/mv0t3Dy.png'),
                        'pseudo': simplegui.load_image('https://imgur.com/lrTqNGD.png'),
                        'icon': simplegui.load_image('https://imgur.com/ApYDvNL.png'),
                        'icon-shaded': simplegui.load_image('https://imgur.com/GvhCpiF.png'),
                        'icon-info': [880, 880],
                        'info': [1400, 650],
                        'size': [200, 100],
                        'cost': 3,
                        'info-pic': simplegui.load_image('https://imgur.com/FZo2aNQ.png')
                       },
               'fox': {
                        'img': simplegui.load_image('https://imgur.com/ovqOwge.png'),
                        'special': simplegui.load_image('https://imgur.com/T2VqmWY.png'),
                        'pseudo': simplegui.load_image('https://imgur.com/aeEfchA.png'),
                        'icon': simplegui.load_image('https://imgur.com/mjuSNgJ.png'),
                        'icon-shaded': simplegui.load_image('https://imgur.com/DuWfYhO.png'),
                        'icon-info': [150, 150],
                        'info': [1600, 1600],
                        'size': [200, 200],
                        'cost': 12,
                        'info-pic': simplegui.load_image('https://imgur.com/eOvRThN.png')
                       },
               
               'mashu': {
                         'img': simplegui.load_image('https://imgur.com/BpewDSD.png'),
                         'special': simplegui.load_image('https://imgur.com/Lr7XvPO.png'),
                         'pseudo': simplegui.load_image('https://imgur.com/NogI2oZ.png'),
                         'icon': simplegui.load_image('https://imgur.com/AlDF1q3.png'),
                         'icon-shaded': simplegui.load_image('https://imgur.com/XsydQla.png'),
                         'icon-info': [200, 200],
                         'info': [1000, 1000],
                         'size': [100, 100],
                         'cost': 5,
                         'info-pic': simplegui.load_image('https://imgur.com/muqrCqG.png')
                        }, 
               
               'ishtar': {
                         'img': simplegui.load_image('https://imgur.com/Y7AI1kU.png'),
                         'special': simplegui.load_image('https://imgur.com/36ULA8o.png'),
                         'pseudo': simplegui.load_image('https://imgur.com/XUNsP4F.png'),
                         'icon': simplegui.load_image('https://imgur.com/Uvh0OSb.png'),
                         'icon-shaded': simplegui.load_image('https://imgur.com/ejcAeWF.png'),
                         'icon-info': [200, 200],
                         'info': [1200, 1200],
                         'size': [140, 140],
                         'cost': 8,
                         'info-pic': simplegui.load_image('https://imgur.com/AAqMCRP.png')
                         }, 
              
               'healer': {
                         'img': simplegui.load_image('https://imgur.com/T0q7xbH.png'),
                         'special': simplegui.load_image('https://imgur.com/HctrdsL.png'),
                         'pseudo': simplegui.load_image('https://imgur.com/Hpp2IqM.png'),
                         'icon': simplegui.load_image('https://imgur.com/1DAWD1p.png'),
                         'icon-shaded': simplegui.load_image('https://imgur.com/7Pc7Nod.png'),
                         'icon-info': [150, 150],
                         'info': [1000, 1000],
                         'size': [110, 110],
                         'cost': 6,
                         'info-pic': simplegui.load_image('https://imgur.com/QqN0OFa.png')
                         }
                   
              }

screen_images  = {
                    'start_screen': simplegui.load_image('https://imgur.com/fTgqrgJ.png'),
                    'lvl-selection': simplegui.load_image('https://imgur.com/hhunJrA.png'),
                    'pause': simplegui.load_image('https://imgur.com/VjxH90U.png'),
                    'end': simplegui.load_image('https://imgur.com/lSU0sZT.png'),
                    'controls': simplegui.load_image('https://imgur.com/4eWoY6I.png'),
                    'journal': simplegui.load_image('https://imgur.com/3vhjSeW.png'),
                    'lose': simplegui.load_image('https://imgur.com/9Rx9LXq.png')
                }

# used to reset stages
def reset():
    global frames_passed
    global hp
    global currency
    global delta_time
    global previous_time
    global placed_units
    global enemies_spawned
    global placed_units_names
    
    
    frames_passed = 0
    hp = 3
    currency = 0
    delta_time = 0
    previous_time = time.time()
    placed_units = []
    enemies_spawned = []
    placed_units_names = []

# creates the 4 directional ranges for each unit
def create_range(offset, unit):
    
    left = []
    # left
    for x in range(offset[0] + 1):
        x_offset = int(math.ceil(unit.position[0] / 100.0)) - x
        y_offset = int(math.ceil(unit.position[1] / 100.0)) 
        left.append([x_offset, y_offset])
                       
        if offset[1] != 0:
            for y in range(1, offset[1] + 1):
                y_offset = int(math.ceil(unit.position[1] / 100.0)) - y
                left.append([x_offset, y_offset])
                y_offset2 = int(math.ceil(unit.position[1] / 100.0)) + y
                left.append([x_offset, y_offset2])
                                
    right = []
    # left
    for x in range(offset[0] + 1):
        x_offset = int(math.ceil(unit.position[0] / 100.0)) + x
        y_offset = int(math.ceil(unit.position[1] / 100.0))
        right.append([x_offset, y_offset])
                       
        if offset[1] != 0:
            for y in range(1, offset[1] + 1):
                y_offset = int(math.ceil(unit.position[1] / 100.0)) - y
                right.append([x_offset, y_offset])
                y_offset2 = int(math.ceil(unit.position[1] / 100.0)) + y
                right.append([x_offset, y_offset2])
                                
    up = []
    # left
    for y in range(offset[0] + 1):
        y_offset = int(math.ceil(unit.position[1] / 100.0)) - y
        x_offset = int(math.ceil(unit.position[0] / 100.0))
        up.append([x_offset, y_offset])
                       
        if offset[1] != 0:
            for x in range(1, offset[1] + 1):
                x_offset = int(math.ceil(unit.position[0] / 100.0)) - x
                up.append([x_offset, y_offset])
                x_offset2 = int(math.ceil(unit.position[0] / 100.0)) + x
                up.append([x_offset2, y_offset])
      
    down = []
    # left
    for y in range(offset[0] + 1):
        y_offset = int(math.ceil(unit.position[1] / 100.0)) + y
        x_offset = int(math.ceil(unit.position[0] / 100.0)) 
        down.append([x_offset, y_offset])
                       
        if offset[1] != 0:
            for x in range(1, offset[1] + 1):
                x_offset = int(math.ceil(unit.position[0] / 100.0)) - x
                down.append([x_offset, y_offset])
                x_offset2 = int(math.ceil(unit.position[0] / 100.0)) + x
                down.append([x_offset2, y_offset])
    
                               
    return [left, right, up, down]

def draw_unit(itself, canvas, img, img_info, size):
        canvas.draw_image(img, (img_info[0] / 2, img_info[1] / 2), (img_info[0], img_info[1]), itself.position, size)
        
        # draws hp
        max_hp_copy = itself.max_hp
        hp_copy = itself.hp


        canvas.draw_polygon([[itself.position[0] - 30, itself.position[1] + 30], 
                             [itself.position[0] + 30, itself.position[1] + 30],
                             [itself.position[0] + 30, itself.position[1] + 35],
                             [itself.position[0] - 30, itself.position[1] + 35]], 1, 'Grey', 'Grey')

        canvas.draw_polygon([[itself.position[0] - 30, itself.position[1] + 30], 
                             [itself.position[0] + 30 - ((1 - (hp_copy/max_hp_copy)) * 60), itself.position[1] + 30],
                             [itself.position[0] + 30 - ((1 - (hp_copy/max_hp_copy)) * 60), itself.position[1] + 35],
                             [itself.position[0] - 30, itself.position[1] + 35]], 1, 'Green', 'Green')
        
        max_special_gauge_copy = itself.max_special_gauge
        special_gauge_copy = itself.special_gauge
        
        canvas.draw_polygon([[itself.position[0] - 30, itself.position[1] + 35], 
                             [itself.position[0] + 30, itself.position[1] + 35],
                             [itself.position[0] + 30, itself.position[1] + 40],
                             [itself.position[0] - 30, itself.position[1] + 40]], 1, 'Grey', 'Grey')

        canvas.draw_polygon([[itself.position[0] - 30, itself.position[1] + 35], 
                             [itself.position[0] + 30 - ((1 - (special_gauge_copy/max_special_gauge_copy)) * 60), itself.position[1] + 35],
                             [itself.position[0] + 30 - ((1 - (special_gauge_copy/max_special_gauge_copy)) * 60), itself.position[1] + 40],
                             [itself.position[0] - 30, itself.position[1] + 40]], 1, 'orange', 'orange')   

# sets the 2 buttons and depending on which side, will draw the unit info on the oppposite side of the unit placed
def draw_otherInfo(itself, canvas):
    global Rbutton
    global Sbutton

    if itself.position[0] < 600:
        x1, x2, x3, x4 = 800, 1100, 830, 1000
        xS, xR = 750, 850

        Rbutton = Button([xR, 150], 75, 75)
        Sbutton = Button([xS, 150], 75, 75)
                
    else:
        x1, x2, x3, x4 = 100, 400, 130, 200
        xS, xR = 450, 350

        Rbutton = Button([xR, 150], 75, 75)
        Sbutton = Button([xS, 150], 75, 75)
            
    
    
    for sqr in itself.real_range:
            x_sqr = sqr[0] * 100
            y_sqr = sqr[1] * 100
            canvas.draw_polygon([[x_sqr, y_sqr], [x_sqr - 100, y_sqr], [x_sqr - 100, y_sqr - 100], [x_sqr, y_sqr - 100]], 1, 'rgb(255,165,0)', 'rgb(255,165,0, .5)')
    
    canvas.draw_image(units_info[itself.name]['info-pic'], (512 / 2, 724 / 2), (512, 724), [x4, 400], (409.6, 579.2))  
    canvas.draw_image(retreat, (100 / 2, 100 / 2), (100,100), [xR, 150], (75, 75))
    canvas.draw_image(special, (100 / 2, 100 / 2), (100,100), [xS, 150], (75, 75))
    return x1, x2, x3, x4
        
def spawn_enemy(stage_lvl):
    global frames_passed
    global bug
    global fly
    
    # hp, damage, move_speed, position, range, enemy_type, enemy_name, currency
    for i in stage_lvl:
        if frames_passed == i[1]:
            if i[0] == 'bug':
                new_enemy = Enemy(4, 1, 2, [stages[currentlvl]['trail'][0][0], stages[currentlvl]['trail'][0][1]], 30, 'ground', 'bug', 1)
                
            elif i[0] == 'fly':
                new_enemy = Enemy(4, 1, 2, [stages[currentlvl]['trail'][0][0], stages[currentlvl]['trail'][0][1]], 100, 'air', 'fly', 1)
                
            elif i[0] == 'spider':
                new_enemy = Enemy(2, 1, 2.5, [stages[currentlvl]['trail'][0][0], stages[currentlvl]['trail'][0][1]], 50, 'ground', 'spider', 1)
              
            elif i[0] == 'laser':
                new_enemy = Enemy(8, 1, 1, [stages[currentlvl]['trail'][0][0], stages[currentlvl]['trail'][0][1]], 150, 'ground', 'laser', 1)
                
            elif i[0] == 'radiance':
                new_enemy = Enemy(30, 3, .5, [stages[currentlvl]['trail'][0][0], stages[currentlvl]['trail'][0][1]], 150, 'air', 'radiance', 1)
                new_enemy.aoeOrNot = True
                new_enemy.aoe_range = 150
                
            elif i[0] == 'caster':
                new_enemy = Enemy(10, 2, 1, [stages[currentlvl]['trail'][0][0], stages[currentlvl]['trail'][0][1]], 150, 'ground', 'caster', 1)
                new_enemy.aoeOrNot = True
                
            elif i[0] == 'kamikaze':
                new_enemy = Enemy(4, 4, 5, [stages[currentlvl]['trail'][0][0], stages[currentlvl]['trail'][0][1]], 80, 'ground', 'kamikaze', 1)
                new_enemy.explodeOrNot = True
                
            elif i[0] == 'knight':
                new_enemy = Enemy(12, 2, 1, [stages[currentlvl]['trail'][0][0], stages[currentlvl]['trail'][0][1]], 80, 'ground', 'knight', 1)
                
            enemies_spawned.append(new_enemy)

# finds trail, so melee units can only be placed on trails, and ranged units must be placed everywhere but trail
def find_can_place(stage_real):
    stage = stage_real.copy()
    stage = [[math.ceil(i[0]/100),math.ceil(i[1]/100)] for i in stage]
    stage[0] = [stage[0][0] + 1, stage[0][1]]
    
    part = 1
    temp = stage[0].copy()
    ground = []
    ground.append(stage[0])
    # [[1, 3], [5, 3], [5, 5], [12, 5]]
    
    while temp != stage[-1]:
        if part != len(stage):
                if stage[part][0] - temp[0] == 0 and stage[part][1] - temp[1] == 0:
                    part += 1

                else:
                    if stage[part][0] - temp[0] > 0:
                        temp[0] += 1
                    
                    elif stage[part][0] - temp[0] < 0:
                        temp[0] -= 1
                    
                    elif stage[part][1] - temp[1] > 0:
                        temp[1] += 1
                    
                    elif stage[part][1] - temp[1] < 0:
                        temp[1] -= 1
                    
                    ground.append(temp.copy())

                    
                
    return ground

# finds which units are on the field
def update_onfield():
    global placed_units_names
    temp = []
    for i in placed_units:
        temp.append(i.name)
        
    placed_units_names = temp      
    
# draws the bottom icons based on your squad characters       
def draw_icon(canvas):
    global state
    global currency
    global character_selected
    
    circle = simplegui.load_image('https://imgur.com/jt1aZeN.png')
    
  
    def draw_only_icon(icon, info, counter, counter2, canvas):
        canvas.draw_image(icon, (info[0] / 2, info[1] / 2), 
                              (info[0], info[1]), [counter, counter2], (150, 150))
    
    
     #draws icons of each unit
    counter = 1125
    counter2 = 875
    for char in squad:
        
        if char == character_selected and state != 'select':
            draw_only_icon(circle, [150, 150], counter, counter2, canvas)
            
        elif char not in placed_units_names and currency >= units_info[char]['cost']:
            draw_only_icon(units_info[char]['icon'], units_info[char]['icon-info'], counter, counter2, canvas)
            
        elif char in placed_units_names or currency < units_info[char]['cost']:
            draw_only_icon(units_info[char]['icon-shaded'], units_info[char]['icon-info'], counter, counter2, canvas)
            
        
        counter -= 150     
        
# buttons for all the icons of charactesr at the bottom        
def create_button():
    counter = 1125
    counter2 = 875
    for char in squad:
        units_info[char]['button'] = Button([counter, counter2], 150, 150)
        counter -= 150
 
# needed for displaying important info within gameplay
def draw_hud(canvas):
    global currency
    global hp
    
    # currency
    currency_img = simplegui.load_image('https://imgur.com/KpoRptB.png')
    canvas.draw_image(currency_img, (420 / 2, 420 / 2), (420, 420), [1120, 760], (40, 40))
    canvas.draw_polygon([(1200, 780), (1200, 740), (1100, 740), (1100, 780)], 3, 'white')
    canvas.draw_text(str(currency), (1150, 770), 30, 'white', 'sans-serif')
    
    # hp
    hp_img = simplegui.load_image('https://imgur.com/59bDKCf.png')
    
    canvas.draw_polygon([(600, 40), (600, 2), (700, 2), (700, 40)], 3, 'white', 'black')
    canvas.draw_image(hp_img, (200 / 2, 200 / 2), (200, 200), [625, 20], (40, 40))
    canvas.draw_text(str(hp), [640, 32], 30, 'white', 'sans-serif')
    
    # enemies left
    canvas.draw_polygon([(500, 40), (500, 2), (600, 2), (600, 40)], 3, 'white', 'black')
    canvas.draw_text(str(currentlvl_left) + '/' + str(len(stages[currentlvl]['spawn'])), [520, 32], 30, 'white', 'sans-serif')
        
def block_attack_units():
    global placed_units
    global enemies_spawned
    global currency
    global currentlvl_left
    
    # for each unit, checks if there is enemy or not. 
    for units in placed_units:

        for enemy in enemies_spawned:
            
            
            if [int(math.ceil(enemy.position[0] / 100.0)), int(math.ceil(enemy.position[1] / 100.0))] not in units.real_range and enemy in units.blocking:
                units.blocking.remove(enemy)
            
            if [int(math.ceil(enemy.position[0] / 100.0)), int(math.ceil(enemy.position[1] / 100.0))] in units.real_range and enemy not in units.blocking and enemy.enemy_type in units.type_target:
                units.blocking.append(enemy)
                
                
                
    # kill enemies and reset their bools and unit values
    for units in placed_units:        
        units.attack()
       

        # add values after kill (currency)
        for enemy in enemies_spawned:
            if enemy.hp <= 0:
                currentlvl_left -= 1
                
                if units.special_gauge < units.max_special_gauge:
                    units.special_gauge += 1
                    
                enemies_spawned.remove(enemy)
                if currency < 15:
                    currency += enemy.currency
                
                for unit in placed_units:
                    if enemy in unit.blocking:
                        unit.blocking.remove(enemy) 

                    if enemy in unit.under_attack:
                        unit.under_attack.remove(enemy)
                                      
def block_attack_enemies():
    global placed_units
    global enemies_spawned
    
    # takes in enemy, and their ranges. And lets them attack towers
    for enemy in enemies_spawned:
        
        for units in placed_units:
            
            if inRange(enemy, units) and enemy not in units.under_attack and len(units.under_attack) < units.can_block:
                units.under_attack.append(enemy)
                enemy.already_attacking = True
            
            elif len(placed_units) == 0:
                enemy.already_attacking = False
                
            elif not inRange(enemy, units) and enemy in units.under_attack and enemy.already_attacking:
                units.under_attack.remove(enemy)
                enemy.already_attacking = False
                
     
    # enemy attack towers, and reset their values
    for enemy in enemies_spawned:
        enemy.reached_end(stages[currentlvl]['trail'])
        found = False
        for units in placed_units:
            if enemy in units.under_attack:
                found = True
                enemy.attack(units)
                
                for unit in placed_units:
                    if unit.hp <= 0:
                        placed_units.remove(unit)
                        for enemy in units.under_attack:
                            enemy.already_blocked = False
                            enemy.already_attacking = False

        enemy.moveOrNot = not found
        if enemy.enemy_name == 'spider':
            enemy.moveOrNot = True

        if enemy.moveOrNot:
                enemy.move(stages[currentlvl]['trail'])
                
def draw_aoe(middle, radius):
    global canvas_copy
    canvas_copy.draw_circle(middle, radius, 2, 'blue', 'blue')
    
def draw_attack_aoe(middle, radius):
    global canvas_copy
    canvas_copy.draw_circle(middle, radius, 2, 'red', 'red')
    
def draw_attack(itself, target):
        global canvas_copy
        timer_started = frames_passed
        canvas_copy.draw_line(itself.position, target.position, 7, 'blue')
        
def draw_enemy_attack(itself, target):
        global canvas_copy
        timer_started = frames_passed
        canvas_copy.draw_line(itself.position, target.position, 4, 'red')
        
def draw_heal(target):
    global canvas_copy

    heal = simplegui.load_image('https://imgur.com/QI8IJpf.png')
    canvas_copy.draw_image(heal, (500 / 2, 500 / 2), (500, 500), target.position, (60, 60))        
   
# detect enemy, if in range
def inRange(obj1, obj_found):
    a = (obj1.position[0] - obj_found.position[0]) ** 2
    b = (obj1.position[1] - obj_found.position[1]) ** 2
    distance = math.sqrt(a + b)

    if distance < obj1.range:
        return True
    else:
        return False
                 
def cancel_selection():
    global state
    global character_selected
    global pseudo_place
    
    state = 'select'
    character_selected = ''
    pseudo_place = None
     
# checks if your either dead or you completed the level
def game_over():
    
    global game_screen
    global hp
    global frame
    if hp <= 0:
        frame.set_mouseclick_handler(start_mouse_handler)
        game_screen = 'lose'
        frame.set_draw_handler(death_screen)
        
    elif currentlvl_left == 0:
        frame.set_draw_handler(end_lvl)
        game_screen = 'end lvl'
        frame.set_mouseclick_handler(start_mouse_handler)
        
        
# draw functions for each screen        
def end_lvl(canvas):
    canvas.draw_image(screen_images['end'], (1200 / 2, 950 / 2), (1200, 950), (1200 / 2, 950 / 2), (1200, 950))

def pause(canvas):
    canvas.draw_image(screen_images['pause'], (1200 / 2, 950 / 2), (1200, 950), (1200 / 2, 950 / 2), (1200, 950))
    
def lvl_selection(canvas):
    canvas.draw_image(screen_images['lvl-selection'], (1200 / 2, 950 / 2), (1200, 950), (1200 / 2, 950 / 2), (1200, 950))
    
def start_screen(canvas):
    music[current_music].play()
    frame.set_mouseclick_handler(start_mouse_handler)
    canvas.draw_image(screen_images['start_screen'], (1200 / 2, 950 / 2), (1200, 950), (1200 / 2, 950 / 2), (1200, 950))
    
def death_screen(canvas):
    canvas.draw_image(screen_images['lose'], (1200 / 2, 950 / 2), (1200, 950), (1200 / 2, 950 / 2), (1200, 950))
  
def control_screen(canvas):
    canvas.draw_image(screen_images['controls'], (1200 / 2, 950 / 2), (1200, 950), (1200 / 2, 950 / 2), (1200, 950))

def journal_screen(canvas):
    canvas.draw_image(screen_images['journal'], (1200 / 2, 950 / 2), (1200, 950), (1200 / 2, 950 / 2), (1200, 950))
    

    
    
    
def create_menu_buttons(): 
    global selection
    global journal
    global controls
    global stage1
    global stage2
    global stage3
    global menu
    global stage_selection
    global stage
    global menu2
    
    # menu buttons
    selection = Button([600, 440], 600, 100)
    controls = Button([585, 544], 300, 90)
    journal = Button([585, 644], 300, 90)

    # stage selection
    stage1 = Button([592, 287], 300, 100)
    stage2 = Button([592, 435], 300, 100)
    stage3 = Button([592, 580], 300, 100)

    # pause menu buttons
    menu = Button([600, 525], 300, 100)
    stage_selection = Button([600, 670], 300, 100)

    # end lvl buttons
    stage = Button([610, 565], 300, 100)
    menu2 = Button([600, 675], 300, 100)
    
# simple enemy
class Enemy():
    def __init__(self, hp, damage, move_speed, position, range, enemy_type, enemy_name, currency):
        self.hp = hp
        self.max_hp = hp
        self.damage = damage
        self.move_speed = move_speed
        self.max_speed = move_speed
        self.position = position
        self.stage_part = 1
        self.range = range
        self.moveOrNot = True
        self.already_attacking = False
        self.already_blocked = False
        self.enemy_type = enemy_type
        self.enemy_name = enemy_name
        self.currency = currency
        self.timer = 0
        self.aoeOrNot = False
        self.aoe_range = 100
        self.explode_range = 300
        self.explodeOrNot = False
        
           
    
    def move(self, stage):
        
        if self.stage_part != len(stage):
            if stage[self.stage_part][0] - self.position[0] == 0 and stage[self.stage_part][1] - self.position[1] == 0:
                self.position[1] = stage[self.stage_part][1]
                self.position[0] = stage[self.stage_part][0]
                self.stage_part += 1
                
            elif abs(stage[self.stage_part][0] - self.position[0]) < self.move_speed and abs(stage[self.stage_part][1] - self.position[1]) < self.move_speed:
                self.position[1] = stage[self.stage_part][1]
                self.position[0] = stage[self.stage_part][0]
                self.stage_part += 1
                
            else:
                if stage[self.stage_part][0] - self.position[0] > 0:
                    self.position[0] += self.move_speed
                elif stage[self.stage_part][0] - self.position[0] < 0:
                    self.position[0] -= self.move_speed
                elif stage[self.stage_part][1] - self.position[1] > 0:
                    self.position[1] += self.move_speed
                elif stage[self.stage_part][1] - self.position[1] < 0:
                    self.position[1] -= self.move_speed
        
        
    
    def attack(self, attack_who):
        
        # aoe enemies attack
        if self.aoeOrNot:
            if self.timer >= 2:
                middle = attack_who.position  
                for units in placed_units:
                    x = (middle[0] - units.position[0]) ** 2
                    y = (middle[1] - units.position[1]) ** 2
                    distance = math.sqrt(x + y)
                    if distance < self.aoe_range:
                        units.hp -= self.damage
                        draw_attack_aoe(middle, self.aoe_range)
                        self.timer = 0

            
        # suicide bombers attack  
        elif self.explodeOrNot:
            middle = self.position  
            for units in placed_units:
                x = (middle[0] - units.position[0]) ** 2
                y = (middle[1] - units.position[1]) ** 2
                distance = math.sqrt(x + y)
                if distance < self.explode_range:
                    units.hp -= self.damage
                    draw_attack_aoe(middle, self.explode_range)
            self.hp -= self.hp
            
        # default enemy attack
        else:
            if self.timer >= 1:
                attack_who.hp -= self.damage
                self.timer = 0
                draw_enemy_attack(self, attack_who)
                
                

    
                    
    # lhandles hp and enemies alive once they reach the end   
    def reached_end(self, currentlvl):
        global currentlvl_left
        global enemies_spawned
        global hp
        if self.position == currentlvl[-1]:
            enemies_spawned.remove(self)
            hp -= 1
            currentlvl_left -= 1
            
    
     
    # displays character when placed
    def draw(self, canvas, img, img_info, SPRITE_SIZE):
        self.timer += delta_time
        
        # draws hp
        max_hp_copy = self.max_hp
        hp_copy = self.hp

        canvas.draw_image(img, (img_info[0] / 2, img_info[1] / 2), (img_info[0], img_info[1]), self.position, SPRITE_SIZE)
        canvas.draw_polygon([[self.position[0] - 30, self.position[1] + 30], 
                             [self.position[0] + 30, self.position[1] + 30],
                             [self.position[0] + 30, self.position[1] + 35],
                             [self.position[0] - 30, self.position[1] + 35]], 1, 'Grey', 'Grey')

        canvas.draw_polygon([[self.position[0] - 30, self.position[1] + 30], 
                             [self.position[0] + 30 - ((1 - (hp_copy/max_hp_copy)) * 60), self.position[1] + 30],
                             [self.position[0] + 30 - ((1 - (hp_copy/max_hp_copy)) * 60), self.position[1] + 35],
                             [self.position[0] - 30, self.position[1] + 35]], 1, 'Green', 'Green')
   
        #canvas.draw_circle(self.position, self.range, 2, 'red')
        
# melee tower/unit    
class nero():
    def __init__(self):
        self.hp = 10
        self.max_hp = 10
        self.damage = 1
        self.can_block = 2
        self.cost = 3
        self.position = []
        self.range = []
        self.special_range = []
        self.real_range = [] # range when placed down
        self.blocking = []
        self.under_attack = []
        self.type_target = 'ground'
        self.name = 'nero'
        self.direction = None
        self.special_gauge = 0
        self.max_special_gauge = 5
        self.timer = 0
        self.specialOrNot = False
        self.startSpecialTimer = 0
        self.attackTimer = 0
        
    
    def draw(self, canvas, img, img_info, size):
        self.timer += delta_time
        self.attackTimer += delta_time
        
        
        draw_unit(self, canvas, img, img_info, size)
        
        
    def draw_info(self, canvas):
 
        x1, x2, x3, x4 = draw_otherInfo(self, canvas)
                      
        # draws info 
        draw_otherInfo(self, canvas)
        canvas.draw_polygon([[x1, 300], [x2, 300], [x2, 500], [x1, 500]], 1, 'rgb(0,0,0, .8)', 'rgb(0,0,0, .8)')
        canvas.draw_text('NERO', (x3, 340), 24, 'white', 'serif')
        canvas.draw_text('Class: guard (can block 2)', (x3, 370), 24, 'white', 'serif')
        canvas.draw_text('Special: extends range by', (x3, 403), 20, 'white', 'serif')
        canvas.draw_text('2, and attack 4 at once', (x3, 433), 20, 'white', 'serif')   
                
    
    def attack(self):
        # every second, a attack is run, depending whether special or not different attacks will happen
        if self.attackTimer >= 1:
            if self.specialOrNot:
                for i in self.blocking:
                    i.hp -= self.damage
                    self.attackTimer = 0
                    draw_attack(self, i)
            else:
                if self.blocking:
                    self.blocking[0].hp -= self.damage
                    self.attackTimer = 0
                    draw_attack(self, self.blocking[0])
                
            
       
    # sets bools and changes info once special is activated
    def special(self):
        self.can_block = 4
        self.real_range = self.special_range[self.direction]
        self.specialOrNot = True
        if self.timer >= (self.startSpecialTimer + 10):
            self.can_block = 2
            self.real_range = self.range[self.direction]
            self.specialOrNot = False
            self.special_gauge = 0          
    
class fox():
    def __init__(self):
        self.hp = 5
        self.max_hp = 5
        self.damage = 2
        self.can_block = 1
        self.cost = 10
        self.aoe_range = 80
        self.position = []
        self.range = []
        self.real_range = [] # range when placed down
        self.blocking = []
        self.under_attack = []
        self.type_target = 'ground air'
        self.name = 'fox'
        self.direction = None
        self.special_gauge = 0
        self.max_special_gauge = 10
        self.timer = 0
        self.specialOrNot = False
        self.startSpecialTimer = 0
        self.attackTimer = 0

    
    def draw(self, canvas, img, img_info, size):
      
        self.timer += delta_time
        self.attackTimer += delta_time
        draw_unit(self, canvas, img, img_info, size)
        
        
    def draw_info(self, canvas):
       
        x1, x2, x3, x4 = draw_otherInfo(self, canvas)
                      
        # draws info        
        draw_otherInfo(self, canvas)
        
        canvas.draw_polygon([[x1, 300], [x2, 300], [x2, 500], [x1, 500]], 1, 'rgb(0,0,0, .8)', 'rgb(0,0,0, .8)')
        canvas.draw_text('Tamamo no Mae', (x3, 340), 24, 'white', 'serif')
        canvas.draw_text('Class: caster (aoe attack)', (x3, 375), 24, 'white', 'serif')
        canvas.draw_text('Special: instantly kills all', (x3, 405), 24, 'white', 'serif')
        canvas.draw_text('enemy on the field', (x3, 435), 24, 'white', 'serif')
        
       
    
    def attack(self):
        # kills everything on the map
        if self.attackTimer >= 2:
            if self.specialOrNot:
                for i in enemies_spawned:
                    i.hp -= i.hp
                    self.attackTimer = 0
            else:
                # normal aoe attack every 2 seconds
                if self.blocking:
                    # aoe attack
                    middle = self.blocking[0].position  
                    self.blocking[0].hp -= self.damage
                    for enemies in enemies_spawned:
                        x = (middle[0] - enemies.position[0]) ** 2
                        y = (middle[1] - enemies.position[1]) ** 2
                        distance = math.sqrt(x + y)
                        if distance < self.aoe_range and enemies.enemy_type in self.type_target:
                            enemies.hp -= self.damage
                            draw_aoe(middle, self.aoe_range)
                            self.attackTimer = 0
      
    
    def special(self):
        self.specialOrNot = True
        self.damage = 5
        if self.timer >= (self.startSpecialTimer + 1):
            self.specialOrNot = False
            self.special_gauge = 0
                
class healer():
    def __init__(self):
        self.hp = 5
        self.max_hp = 5
        self.damage = 2
        self.can_block = 1
        self.cost = 9
        self.position = []
        self.range = []
        self.real_range = [] # range when placed down
        self.blocking = []
        self.under_attack = []
        self.type_target = 'ground air'
        self.name = 'healer'
        self.direction = None
        self.special_gauge = 0
        self.max_special_gauge = 5
        self.timer = 0
        self.specialOrNot = False
        self.startSpecialTimer = 0
        self.attackTimer = 0

    
    def draw(self, canvas, img, img_info, size):
        self.timer += delta_time
        self.attackTimer += delta_time
        
        
        draw_unit(self, canvas, img, img_info, size)
        
        
    def draw_info(self, canvas):
        

        x1, x2, x3, x4 = draw_otherInfo(self, canvas)
                      
        # draws info   
        draw_otherInfo(self, canvas)
        canvas.draw_polygon([[x1, 300], [x2, 300], [x2, 500], [x1, 500]], 1, 'rgb(0,0,0, .8)', 'rgb(0,0,0, .8)')
        canvas.draw_text('Marie Antoinette', (x3, 340), 24, 'white', 'serif')
        canvas.draw_text('Class: Healer (only heals', (x3, 375), 24, 'white', 'serif')
        canvas.draw_text('cant block or attack)', (x3, 405), 24, 'white', 'serif')
        canvas.draw_text('Special: instantly heal allies', (x3, 435), 24, 'white', 'serif')
        canvas.draw_text('(charges every 2 seconds)', (x3, 465), 24, 'white', 'serif')
        

    
    def attack(self):
        # instantly heals all enemies
        if self.specialOrNot:
                for i in placed_units:
                    i.hp = i.max_hp
                    draw_heal(i)
        
        # every 4 seconds, heal a unit with hp loss
        if self.attackTimer >= 4:
            
            if not self.specialOrNot:
                healing = None
                for i in placed_units:
                    if [math.ceil(i.position[0] / 100), math.ceil(i.position[1] / 100)] in self.real_range and i.name != 'healer' and i.hp < i.max_hp:
                        healing = i
                if healing:         
                    healing.hp += 1
                    draw_heal(healing)
                    
                self.attackTimer = 0
            
       
    
    def special(self):
        self.specialOrNot = True
        if self.timer >= (self.startSpecialTimer + 1):
            self.specialOrNot = False
            self.special_gauge = 0           
                      
class mashu():
    def __init__(self):
        self.hp = 20
        self.max_hp = 20
        self.damage = 1
        self.can_block = 5
        self.cost = 5
        self.position = []
        self.range = []
        self.real_range = [] # range when placed down
        self.blocking = []
        self.under_attack = []
        self.type_target = 'ground'
        self.name = 'mashu'
        self.direction = None
        self.special_gauge = 0
        self.max_special_gauge = 5
        self.timer = 0
        self.specialOrNot = False
        self.startSpecialTimer = 0
        self.attackTimer = 0
        
    
    def draw(self, canvas, img, img_info, size):

        self.timer += delta_time
        self.attackTimer += delta_time
        
        
        draw_unit(self, canvas, img, img_info, size)
        
        
    def draw_info(self, canvas):

 
        x1, x2, x3, x4 = draw_otherInfo(self, canvas)
                      
        # draws info   
        draw_otherInfo(self, canvas)
        canvas.draw_polygon([[x1, 300], [x2, 300], [x2, 500], [x1, 500]], 1, 'rgb(0,0,0, .8)', 'rgb(0,0,0, .8)')
        canvas.draw_text('Mashu Kyrielight', (x3, 340), 24, 'white', 'serif')
        canvas.draw_text('Class: tank (blocks 5)', (x3, 375), 24, 'white', 'serif')
        canvas.draw_text('Special: slows down all', (x3, 405), 24, 'white', 'serif')
        canvas.draw_text('enemies by half their', (x3, 435), 24, 'white', 'serif')
        canvas.draw_text('normal speed', (x3, 465), 24, 'white', 'serif')

        # draws the retreat and special button
        
                
    
    def attack(self):
        # slows down all enemies by half
        if self.specialOrNot:
            for enemies in enemies_spawned:
                enemies.move_speed = enemies.max_speed / 2
                
        if self.attackTimer >= 1:
            if self.blocking:
                self.blocking[0].hp -= self.damage
                
            self.attackTimer = 0
       
    
    def special(self):
        
        self.specialOrNot = True
        if self.timer >= (self.startSpecialTimer + 10): 
            for enemies in enemies_spawned:
                enemies.move_speed = enemies.max_speed
            self.specialOrNot = False
            self.special_gauge = 0
      
class ishtar():
    def __init__(self):
        self.hp = 8
        self.max_hp = 8
        self.damage = 2
        self.special_damage = 5
        self.can_block = 1
        self.cost = 4
        self.position = []
        self.range = []
        self.special_range = []
        self.real_range = [] # range when placed down
        self.blocking = []
        self.under_attack = []
        self.type_target = 'ground air'
        self.name = 'ishtar'
        self.direction = None
        self.special_gauge = 0
        self.max_special_gauge = 5
        self.timer = 0
        self.specialOrNot = False
        self.startSpecialTimer = 0
        self.attackTimer = 0
        
    
    def draw(self, canvas, img, img_info, size):

        self.timer += delta_time
        self.attackTimer += delta_time
        
        
        draw_unit(self, canvas, img, img_info, size)
        
        
    def draw_info(self, canvas):
        

 
        x1, x2, x3, x4 = draw_otherInfo(self, canvas)
                      
        # draws info     
        draw_otherInfo(self, canvas)
        canvas.draw_polygon([[x1, 300], [x2, 300], [x2, 500], [x1, 500]], 1, 'rgb(0,0,0, .8)', 'rgb(0,0,0, .8)')
        canvas.draw_text('Ishtar', (x3, 340), 24, 'white', 'serif')
        canvas.draw_text('Class: Sniper (block 1)', (x3, 375), 24, 'white', 'serif')
        canvas.draw_text('Special: extends range', (x3, 405), 24, 'white', 'serif')
        canvas.draw_text('and damage increases', (x3, 435), 24, 'white', 'serif')
        canvas.draw_text('slower atk speed', (x3, 465), 24, 'white', 'serif')
        
        # draws the retreat and special button
        
    
    
    def attack(self):  
        if self.specialOrNot:

            if self.attackTimer >= 2:

                if self.blocking:
                    self.blocking[0].hp -= self.damage
                    draw_attack(self, self.blocking[0])
                    self.attackTimer = 0
                
        else:
            if self.attackTimer >= 2:
                if self.blocking:
                    self.blocking[0].hp -= self.damage

                    
                    draw_attack(self, self.blocking[0])
                    self.attackTimer = 0
       
    
    def special(self):
        self.real_range = self.special_range[self.direction]
        self.damage = self.special_damage
        self.specialOrNot = True
       
        if self.timer >= (self.startSpecialTimer + 10): 
            self.real_range = self.range[self.direction]
            self.specialOrNot = False
            self.special_gauge = 0     

class Button:
    def __init__(self, location, width, height):
        self.pos = location
        self.width = width
        self.height = height
        
    def is_selected(self, mouse_pos):
        left = self.pos[0] - self.width/2
        right = self.pos[0] + self.width/2
        top = self.pos[1] - self.height/2
        bottom = self.pos[1] + self.height/2
        in_x = mouse_pos[0] >= left and mouse_pos[0] <= right
        in_y = mouse_pos[1] >= top and mouse_pos[1] <= bottom
        return in_x and in_y
    
    
    
create_menu_buttons()    

# mouse handler for navigating screens
def start_mouse_handler(position):
    global game_screen
    global currentlvl
    global currentlvl_left
    global enemies_spawned
    global placed_units
    global squad
    global current_music
    
    # route for menu screen
    if game_screen == 'menu':
     
        if selection.is_selected(position):
            frame.set_draw_handler(lvl_selection)
            game_screen = 'stage-selection'

        elif controls.is_selected(position):
            frame.set_draw_handler(control_screen)
            game_screen = 'controls'
            
        elif journal.is_selected(position):
            frame.set_draw_handler(journal_screen)
            game_screen = 'journal'
        
    # routes for stage selection    
    elif game_screen == 'stage-selection':
        if stage1.is_selected(position):
            
            music[current_music].rewind()
            current_music = 'stage1'
            music[current_music].play()
            
            if 'nero' not in squad and 'mashu' not in squad and 'healer' not in squad:
                squad.append('nero')
                squad.append('mashu')
                squad.append('healer')
            create_button()
            frame.set_mouseclick_handler(mouse_handler)
            game_screen = 'ingame1'
            currentlvl = 'stage1'
            reset()
            currentlvl_left = len(stages[currentlvl]['spawn'])
            frame.set_draw_handler(render)
            
        elif stage2.is_selected(position):
            
            music[current_music].rewind()
            current_music = 'stage2'
            music[current_music].play()

            if 'ishtar' not in squad:
                squad.append('ishtar')
            create_button()
            frame.set_mouseclick_handler(mouse_handler)
            game_screen = 'ingame2'
            currentlvl = 'stage2'
            reset()
            currentlvl_left = len(stages[currentlvl]['spawn'])
            frame.set_draw_handler(render)
            
        elif stage3.is_selected(position):
            
            music[current_music].rewind()
            current_music = 'stage3'
            music[current_music].play()

            if 'fox' not in squad:
                squad.append('fox')
            create_button()
            frame.set_mouseclick_handler(mouse_handler)
            game_screen = 'ingame3'
            currentlvl = 'stage3'
            reset()
            currentlvl_left = len(stages[currentlvl]['spawn'])
            frame.set_draw_handler(render)
    
    # route for pause screen
    elif game_screen == 'pause':
        if menu.is_selected(position):
            
            music[current_music].rewind()
            current_music = 'menu'
            music[current_music].play()
            
            frame.set_draw_handler(start_screen)
            game_screen = 'menu'
            
        elif stage_selection.is_selected(position):
            
            music[current_music].rewind()
            current_music = 'menu'
            music[current_music].play()
            
            frame.set_draw_handler(lvl_selection)
            game_screen = 'stage-selection'
            
    # route for win screen
    elif game_screen == 'end lvl' or game_screen == 'lose':
        if stage.is_selected(position):
            music[current_music].rewind()
            current_music = 'menu'
            music[current_music].play()
            frame.set_draw_handler(lvl_selection)
            game_screen = 'stage-selection'
            
        elif menu2.is_selected(position):
            music[current_music].rewind()
            current_music = 'menu'
            music[current_music].play()
            frame.set_draw_handler(start_screen)
            game_screen = 'menu'
                      
# return to previous screen when esc is pressed
def key_handler(key):
    global game_screen
    if game_screen == 'stage-selection' or game_screen == 'controls' or game_screen == 'journal':
        if key == 27:
            frame.set_draw_handler(start_screen)
            game_screen = 'menu'
            
    elif 'ingame' in game_screen:
        if key == 27:
            frame.set_draw_handler(pause)
            frame.set_mouseclick_handler(start_mouse_handler)
            game_screen = 'pause'
            
    elif game_screen == 'pause':
        if key == 27:
            frame.set_draw_handler(render)
            frame.set_mouseclick_handler(mouse_handler)
            game_screen = 'ingame'
      
# mousehandler for ingame
def mouse_handler(position):
    global state
    global pseudo_place
    global mouse_down
    global character_selected
    global placed_units_names
    global currency
    global info_selected

    x = position[0]
    y = position[1]
    
    # changes ur mouse click location, to the center of the coresponding square
    x_placement = (int(math.ceil(position[0] / 100.0)) * 100) - 50
    y_placement = (int(math.ceil(position[1] / 100.0)) * 100) - 50
    can_place = True
    
    # sees if the click was in the icon section or not
    if y > 800:
        can_place = False
        
    # if a unit is already on the sqr u clicked, can place is set to false
    for units in placed_units:
        if (units.position[0] == x_placement and units.position[1] == y_placement): 
            can_place = False
    
    
    # depending on the location of where you click, if its able to be placed, the game will set needed variables, and let you place
    if can_place and state == 'pseudo-place':
        
        if character_selected == 'nero':
            new_unit = nero()
            new_unit.position = [x_placement, y_placement]
            new_unit.range = create_range([1, 0], new_unit)
            new_unit.special_range = create_range([3, 0], new_unit)
        
        if character_selected == 'ishtar':
            new_unit = ishtar()
            new_unit.position = [x_placement, y_placement]
            new_unit.range = create_range([3, 1], new_unit)
            new_unit.special_range = create_range([5, 1], new_unit)
                   
            
        if character_selected == 'mashu':
            new_unit = mashu()
            new_unit.position = [x_placement, y_placement]
            new_unit.range = create_range([0, 0], new_unit)
            
        if character_selected == 'fox':
            new_unit = fox()
            new_unit.position = [x_placement, y_placement]
            new_unit.range = create_range([2, 1], new_unit)
            
        if character_selected == 'healer':
            new_unit = healer()
            new_unit.position = [x_placement, y_placement]
            new_unit.range = create_range([2, 1], new_unit)
            
          
        # if the unit is a ground attacking unit, it means its melee, which this if statement will check if its on the trail or not
        if 'ground' == new_unit.type_target:
            # if on the trail can place
            if [math.ceil(new_unit.position[0] / 100), math.ceil(new_unit.position[1] / 100)] in find_can_place(stages[currentlvl]['trail']):
                pseudo_place = new_unit
                state = 'direction'
        else:
            # if not on the trail and isnt a only ground attacking unit can place
            if [math.ceil(new_unit.position[0] / 100), math.ceil(new_unit.position[1] / 100)] not in find_can_place(stages[currentlvl]['trail']):
                pseudo_place = new_unit
                state = 'direction'
            
            
        
  
    # if ur in selection mode, it will check if you are able to select the character
    for char in squad:
        if units_info[char]['button'].is_selected(position) and state == 'select' and char not in placed_units_names and currency >= units_info[char]['cost']:
            state = 'pseudo-place'
            character_selected = char
        
        # cancel placement
        elif units_info[char]['button'].is_selected(position) and state != 'select' and character_selected == char:
            cancel_selection()
        
    # opepns info if can  
    if state == 'info' and [x_placement, y_placement] != Sbutton.pos and [x_placement, y_placement] != Rbutton.pos:
        state = 'select'
        info_selected = None
        
    # activates the buttons in info mode    
    if state != 'direction2':
    
        for unit in placed_units:
            if unit.position == [x_placement, y_placement]:
                state = 'info'
                info_selected = unit.name

            elif state == 'info' and info_selected == unit.name and unit.special_gauge >= unit.max_special_gauge and Sbutton.is_selected(position):
                unit.startSpecialTimer = unit.timer
                unit.special()

                state = 'select'
                info_selected = None

            elif state == 'info' and info_selected == unit.name and Rbutton.is_selected(position):
                placed_units.remove(unit)
                state = 'select'
                info_selected = None


           
 
    mouse_down = False
  
# drag function, where direction is based on where ur mouse is
mouse_down = True
def mouse_drag(drag):
    global mouse_down
    global count_mouse
    global state
    global pseudo_place
    
    if state == "direction":
        state = "direction2"
        
    
    mouse_down = True
    
    if state == "direction2" and pseudo_place != None:
        x = drag[0] - pseudo_place.position[0]
        y = drag[1] - pseudo_place.position[1]
        if abs(x) > abs(y):
            if x < 0:
                pseudo_place.real_range = pseudo_place.range[0]
                pseudo_place.direction = 0
            else:
                pseudo_place.real_range = pseudo_place.range[1]
                pseudo_place.direction = 1
        elif abs(x) < abs(y):
            if y < 0:
                pseudo_place.real_range = pseudo_place.range[2]
                pseudo_place.direction = 2
            else:
                pseudo_place.real_range = pseudo_place.range[3]
                pseudo_place.direction = 3
                

# main game
def render(canvas):
    global mouse_down
    global frames_passed
    global pseudo_place
    global state
    global enemies_spawned
    global character_selected
    global placed_units_names
    global hp
    global currency
    global canvas_copy
    
    
    global delta_time
    global previous_time
    
    
    canvas_copy = canvas
    
    # counts time passed
    delta_time = time.time() - previous_time
    previous_time = time.time()
    
    # counts frames
    frames_passed += 1
    
    # obtain a currency every 2 seconds
    if frames_passed % 180 == 0 and currency < 15:
        currency += 1
    # every 3 seconds add to special gauge
    for units in placed_units:
        if frames_passed % 180 == 0 and units.special_gauge < units.max_special_gauge:
                units.special_gauge += 1
    
    spawn_enemy(stages[currentlvl]['spawn'])
    game_over()
    update_onfield()
    
    #draws map and grid
    canvas.draw_image(stages[currentlvl]['image'], (1200 // 2, 800 // 2), (1200, 800), (1200//2, 800//2), (1200, 800))
    
    for i in range(1, WIDTH // 100):
        canvas.draw_line((i * 100, 0), (i * 100, HEIGHT - 150), 1, 'white')
    
    for i in range(1, int(math.ceil((HEIGHT / 100) - 2))):
        canvas.draw_line((0, i * 100), (WIDTH, i * 100), 1, 'white')
        
    draw_icon(canvas)
    draw_hud(canvas)
    
    block_attack_units()
    block_attack_enemies()
    
    

    # draws the pseudo characters and their ranges (before the units r placed)
    if pseudo_place != None:
        
        for sqr in pseudo_place.real_range:
            x_sqr = sqr[0] * 100
            y_sqr = sqr[1] * 100
            canvas.draw_polygon([[x_sqr, y_sqr], [x_sqr - 100, y_sqr], [x_sqr - 100, y_sqr - 100], [x_sqr, y_sqr - 100]], 1, 'rgb(255,165,0)', 'rgb(255,165,0, .5)')
        

        pseudo_place.draw(canvas, units_info[character_selected]['pseudo'],units_info[character_selected]['info'], units_info[character_selected]['size'])

    # places down the character when mouse is let go   
    if not mouse_down and pseudo_place != None and state == "direction2":
        placed_units.append(pseudo_place)
        currency -= pseudo_place.cost
        pseudo_place = None
        state = 'select'
        character_selected = ''
        
        
    # draws character that r placed
    for units in placed_units:

        if units.specialOrNot:
            units.draw(canvas, units_info[units.name]['special'], units_info[units.name]['info'], units_info[units.name]['size'])    
        else:
            units.draw(canvas, units_info[units.name]['img'], units_info[units.name]['info'], units_info[units.name]['size'])

        if units.specialOrNot:
            units.special()
    
    #draws enemies on board
    for enemy in enemies_spawned:
        enemy.draw(canvas, enemies_info[enemy.enemy_name]['img'], enemies_info[enemy.enemy_name]['info'], enemies_info[enemy.enemy_name]['size'])

    # draws info of units when selected
    if info_selected != None:
        for i in placed_units:
            if i.name == info_selected:
                i.draw_info(canvas)

     



frame = simplegui.create_frame('Game', WIDTH, HEIGHT)
frame.set_draw_handler(start_screen)
frame.set_keydown_handler(key_handler)
frame.set_mouseclick_handler(mouse_handler)
frame.set_mousedrag_handler(mouse_drag)
frame.start()
