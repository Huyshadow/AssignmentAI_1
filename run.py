import math
import sys

import pygame
import pygame_menu

from game import UI
from algorithmUI import AlgorithmUI_Show, AlgorithUI_Stats

# Global Constants
FPS = 60
NUMBER_OF_LEVELS = 33
LEVEL_PER_ROW = 10

# Global Variables
CURRENT_STATE = 'MENU'
ALGORITHM = 'BFS'

FONT = pygame_menu.font.FONT_OPEN_SANS
FONT_BOLD = pygame_menu.font.FONT_OPEN_SANS_BOLD

LIGHT_BLUE = (16, 109, 191)
DARK_BLUE = (0,0,139)
COLOR_BACKGROUND = (33, 60, 254)

HEIGHT_SIZE = 600 
WIDTH_SIZE = 1000

FONT = pygame_menu.font.FONT_OPEN_SANS
FONT_BOLD = pygame_menu.font.FONT_OPEN_SANS_BOLD

CUSTOME_THEME = pygame_menu.Theme(
    background_color=(255, 255, 255),
    selection_color=LIGHT_BLUE,
    title_background_color=LIGHT_BLUE,
    title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_ADAPTIVE,
    title_font=FONT,
    title_font_antialias=True,
    title_font_color =(255,255,255),
    title_font_size=48,
    widget_font=FONT,
    widget_font_size=32,
    widget_margin=(0,8),
    widget_cursor=pygame_menu.locals.CURSOR_HAND,)

if __name__ =="__main__":
    pygame.init()

    tictok = pygame.time.Clock()

    background = pygame.display.set_mode((WIDTH_SIZE,HEIGHT_SIZE))

    def btn_effect_chosen(selected, widget, menu):
        if selected:
            widget.set_font(font_size=32,color='white',
                            font=FONT_BOLD,
                            background_color=DARK_BLUE,readonly_color=LIGHT_BLUE,
                            readonly_selected_color='white',selected_color='red',)
        else:
            widget.set_font(font_size=32,color='white',
                        font=FONT_BOLD,
                        background_color=LIGHT_BLUE,readonly_color=LIGHT_BLUE,
                        readonly_selected_color='white',selected_color='red',)
    
    #Menu

    def algorithm_chosen_level(level_id):
        global ALGORITHM_STATS, CURRENT_STATE, ALGORITHM, menu 

        #Status 
        ALGORITHM_STATS = AlgorithUI_Stats(background, HEIGHT_SIZE, WIDTH_SIZE, level_id, ALGORITHM)
        menu.disable()
        #---------------
        CURRENT_STATE = 'VIEWING_STATS_ALGORITHM'
    
    def chosen_algorithm(selected_value, algorithm, **kwargs):
        global ALGORITHM
        ALGORITHM = algorithm
    
    algorithm_menu = pygame_menu.Menu('ASS1-Bloxorz', WIDTH_SIZE, HEIGHT_SIZE,
                                    onclose=None,
                                    theme=CUSTOME_THEME,
                                    mouse_motion_selection=True)

    algorithm_menu.add.label('LEVELS',font_size=40)


    algorithm_menu.add.selector('Algorithm', 
                                items=[('BFS','BFS'),('DFS','DFS')],
                                onchange=chosen_algorithm)
    
    # create level table for Level #
    for level_in_row in range(math.ceil(NUMBER_OF_LEVELS/LEVEL_PER_ROW)):
        f = algorithm_menu.add.frame_h(WIDTH_SIZE, 60, margin=(0,0))

        for level_id in range(level_in_row*LEVEL_PER_ROW,
        min((level_in_row+1)*LEVEL_PER_ROW,NUMBER_OF_LEVELS)):
            btn = algorithm_menu.add.button(f' {level_id+1:02d} ',
                                            algorithm_chosen_level,
                                            level_id+1)
            btn.set_margin(0, 0)
            btn.set_padding((4,8))
            btn.set_selection_effect(pygame_menu.widgets.NoneSelection())
            btn.set_selection_callback(btn_effect_chosen)

            f.pack(btn,align='align-center')

    algorithm_menu.add.button('BACK', pygame_menu.events.BACK,font_size=24).translate(300,20)

    # Play menu
    play_menu = pygame_menu.Menu('ASS1-Bloxorz', WIDTH_SIZE, HEIGHT_SIZE,
                                onclose=None,
                                theme=CUSTOME_THEME,
                                mouse_motion_selection=True)

    play_menu.add.button('ASS1-Bloxorz', algorithm_menu)
    play_menu.add.button('BACK', pygame_menu.events.BACK)

     # About menu
    about_menu = pygame_menu.Menu('Bloxorz', WIDTH_SIZE, HEIGHT_SIZE,
                            onclose=None,
                            theme=CUSTOME_THEME,
                            mouse_motion_selection=True)

    about_menu.add.label('ABOUT',font_size=40).translate(0, -40)

    about_menu.add.label('A Blozorx solver ASS1',font_size=25).translate(0, -20)

    """ about_menu.add.label('Author:  Le Nguyen Hung                 -  2013360',font_size=20)
    about_menu.add.label('                Nguyen Van Bao Nguyen  -  2013930',font_size=20)
    about_menu.add.label('                Vo Phan Anh Quan             -  2014285',font_size=20) """

    about_menu.add.button('BACK', pygame_menu.events.BACK, font_size=24).translate(0, 40)


    # Main menu

    menu = pygame_menu.Menu('ASS1-Bloxorz', WIDTH_SIZE, HEIGHT_SIZE,
                            onclose=None,
                            theme=CUSTOME_THEME,
                            mouse_motion_selection=True,)

    menu.add.button('PLAY GAME', play_menu)
    menu.add.button('ABOUT', about_menu)
    menu.add.button('QUIT', pygame_menu.events.EXIT)

    # Main loop
    while True:
        # tick clock
        deltatime = tictok.tick(FPS)

        background.fill(COLOR_BACKGROUND)

        events = pygame.event.get()
        if CURRENT_STATE == 'VIEWING_STATS_ALGORITHM':
            ALGORITHM_STATS.process(events)
            if ALGORITHM_STATS.should_quit():
                CURRENT_STATE = 'MENU'
                menu.enable()
            elif ALGORITHM_STATS.should_show():
                CURRENT_STATE = 'VIEWING_ALGORITHM'
                ALGORITHM_SHOW = AlgorithmUI_Show(background, HEIGHT_SIZE, WIDTH_SIZE, ALGORITHM_STATS.game.level_id.level, ALGORITHM_STATS.show_path(), 300)
        elif CURRENT_STATE == 'VIEWING_ALGORITHM':
            ALGORITHM_SHOW.process(events, deltatime)
            if ALGORITHM_SHOW.should_quit():
                CURRENT_STATE = 'MENU'
                menu.enable()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        try:
            menu.mainloop(background)
        except:
            pass
        
        pygame.display.update()
