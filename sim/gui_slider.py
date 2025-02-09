import pygame as pg

class Slider:
    def __init__(self, name, x, y, width, puck_width, height, value, v_min, v_max, font, screen, container, color=(200,200,200), l_text='left', r_text='right'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.puck_width = puck_width
        self.value = value
        self.v_min = v_min
        self.v_max = v_max
        self.font = font
        self.screen = screen

        self.fillColors = {
            'normal': color,
            'puck': (255, 255, 255),
            'puck_hover': (200, 200, 200)
        }

        self.button_surface = pg.Surface((self.width, self.height))
        # self.button_outline = pg.Rect(self.x, self.y, self.width, self.height)
        self.button_rect = pg.Rect(self.x, self.y, self.width, self.height)
        self.percent_value = 0
        self.refresh_percent_value()
        self.puck_rect = pg.Rect(self.x + ((self.percent_value ** (1/2)) * self.width) - (self.puck_width / 2), self.y, self.puck_width, self.height)
        self.puck_surface = pg.Surface((self.puck_width, self.height))
        self.button_text_surf_l = self.font.render(l_text, True, (20, 20, 20))
        self.button_text_surf_r = self.font.render(r_text, True, (20, 20, 20))
        container.update({name: self})

    def refresh_percent_value(self):
        self.percent_value = max(0, min(100, ((self.value[0] - self.v_min) / (self.v_max - self.v_min))))

    def update_colors(self, color):
        self.fillColors = {
            'normal': color,
            'puck': (255, 255, 255),
            'puck_hover': (200, 200, 200)
        }

    def process(self):
        mouse_pos = pg.mouse.get_pos()
        self.button_surface.fill(self.fillColors['normal'])
        self.puck_surface.fill(self.fillColors['puck'])

        if self.button_rect.collidepoint(mouse_pos):
            self.puck_surface.fill(self.fillColors['puck_hover'])

            if pg.mouse.get_pressed(num_buttons=3)[0]:
                # self.puck_surface.fill(self.fillColors['pressed'])
                mouse_percent = (mouse_pos[0] - self.x) / self.width
                value_percent = self.v_min + ((mouse_percent ** 2) * (self.v_max - self.v_min))
                self.value[0] = max(self.v_min, min(self.v_max, round(value_percent)))
                self.refresh_percent_value()
                self.puck_rect.x = self.x + ((self.percent_value ** (1/2)) * self.width) - (self.puck_width / 2)

        self.button_surface.blit(self.button_text_surf_l, [
            self.button_text_surf_l.get_rect().width / 2,
            self.button_rect.height / 2 - self.button_text_surf_l.get_rect().height / 2
        ])
        self.button_surface.blit(self.button_text_surf_r, [
            self.button_rect.width - self.button_text_surf_r.get_rect().width - self.button_text_surf_r.get_rect().width / 2,
            self.button_rect.height / 2 - self.button_text_surf_r.get_rect().height / 2
        ])
        self.screen.blit(self.button_surface, self.button_rect)
        self.screen.blit(self.puck_surface, self.puck_rect)
