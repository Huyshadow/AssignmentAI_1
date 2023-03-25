import math
import sys,os

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

HEIGHT_SIZE = 800 
WIDTH_SIZE = 1087

FONT = pygame_menu.font.FONT_OPEN_SANS
FONT_BOLD = pygame_menu.font.FONT_OPEN_SANS_BOLD

myimage = pygame_menu.baseimage.BaseImage(
    image_path='./design_game/Background1.png',
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL,
)
CUSTOME_THEME = pygame_menu.Theme(
    background_color=myimage,
    selection_color=LIGHT_BLUE,
    title_background_color=LIGHT_BLUE,
    title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
    title_font=FONT,
    title_font_antialias=True,
    title_font_color =(255,255,255),
    title_font_size=48,
    widget_font=FONT,
    widget_font_size=32,
    widget_margin=(0,8),
    widget_cursor=pygame_menu.locals.CURSOR_HAND,)
class MyButton(pygame_menu.widgets.Button):
    def __init__(self, text, font, *args, **kwargs):
        super().__init__(text, *args, **kwargs)
        self.font = font
        self.font_color = (255, 255, 255)
        self.bg_color = (0, 0, 0)

    def draw(self, surface):
        # Draw the button background
        rect = pygame.Rect(self._rect)
        pygame.draw.rect(surface, self.bg_color, rect)

        # Draw the button label
        font_surface = self.font.render(self.get_title(), True, self.font_color)
        font_rect = font_surface.get_rect(center=rect.center)
        surface.blit(font_surface, font_rect)

if __name__ =="__main__":
    pygame.init()

    tictok = pygame.time.Clock()

    background = pygame.display.set_mode((WIDTH_SIZE,HEIGHT_SIZE))
    charRect = pygame.Rect((0,0),(1087, 800))
    charImage = pygame.image.load(os.path.join("design_game", "Background1.png"))
    charImage = pygame.transform.scale(charImage, charRect.size)
    charImage = charImage.convert()
    background.blit(charImage,charRect)

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
    
    algorithm_menu = pygame_menu.Menu('', WIDTH_SIZE, HEIGHT_SIZE,
                                    onclose=None,
                                    theme=CUSTOME_THEME,
                                    mouse_motion_selection=True)

    algorithm_menu.add.label('LEVELS',font_size=40)


    algorithm_menu.add.selector('Algorithm', 
                                items=[('BFS','BFS'),('DFS','DFS'),('A*','A*')],
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
    play_menu = pygame_menu.Menu('', WIDTH_SIZE, HEIGHT_SIZE,
                                onclose=None,
                                theme=CUSTOME_THEME,
                                mouse_motion_selection=True)

    play_menu.add.button('ALGORITHM', algorithm_menu)
    play_menu.add.button('BACK', pygame_menu.events.BACK)

     # About menu
    about_menu = pygame_menu.Menu('', WIDTH_SIZE, HEIGHT_SIZE,
                            onclose=None,
                            theme=CUSTOME_THEME,
                            mouse_motion_selection=True)

    about_menu.add.label('ABOUT',font_size=40).translate(0, -40)

    about_menu.add.label('A Blozorx solver ASS1 created by',font_size=25).translate(0, -20)

    about_menu.add.label('Author:     Tran Cong Minh Quan  -  2012528',font_size=20)
    about_menu.add.label('                 Thi Khac Quan              -  2011925',font_size=20)
    about_menu.add.label('                 Dang Quang Thanh     -  2014485',font_size=20)
    about_menu.add.label('                 Dang Quang Huy         -  2012504',font_size=20) 

    about_menu.add.button('BACK', pygame_menu.events.BACK, font_size=24).translate(0, 40)


    # Main menu

    menu = pygame_menu.Menu('', WIDTH_SIZE, HEIGHT_SIZE,
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
