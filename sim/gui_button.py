import pygame as pg

class Button:
    def __init__(self, name, x, y, width, height, font, screen, container, color=(200,200,200), button_text='Button', on_click_function=None, one_press=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.on_click_function = on_click_function
        self.one_press = one_press
        self.already_pressed = False
        self.font = font
        self.screen = screen

        self.fillColors = {
            'normal': color,
            'hover': (max(0, color[0] - 25), max(0, color[1] - 25), max(0, color[2] - 25)),
            'pressed': (max(0, color[0] - 40), max(0, color[1] - 40), max(0, color[2] - 40))
        }

        self.button_surface = pg.Surface((self.width , self.height))
        # self.button_outline = pg.Rect(self.x, self.y, self.width, self.height)
        self.button_rect = pg.Rect(self.x, self.y, self.width, self.height)
        self.button_text_surf = self.font.render(button_text, True, (20, 20, 20))
        container.update({name: self})

    def update_colors(self, color):
        self.fillColors = {
            'normal': color,
            'hover': (max(0, color[0] - 25), max(0, color[1] - 25), max(0, color[2] - 25)),
            'pressed': (max(0, color[0] - 40), max(0, color[1] - 40), max(0, color[2] - 40))
        }

    def process(self):
        mouse_pos = pg.mouse.get_pos()
        self.button_surface.fill(self.fillColors['normal'])

        if self.button_rect.collidepoint(mouse_pos):
            self.button_surface.fill(self.fillColors['hover'])
            if pg.mouse.get_pressed(num_buttons=3)[0]:
                self.button_surface.fill(self.fillColors['pressed'])
                if self.one_press:
                    self.on_click_function()
                elif not self.already_pressed:
                    self.on_click_function()
                    self.already_pressed = True
            else:
                self.already_pressed = False

        self.button_surface.blit(self.button_text_surf, [
            self.button_rect.width / 2 - self.button_text_surf.get_rect().width / 2,
            self.button_rect.height / 2 - self.button_text_surf.get_rect().height / 2
        ])

        self.screen.blit(self.button_surface, self.button_rect)
