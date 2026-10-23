import pygame 
from loguru import logger
from numba import njit
import numpy
import cv2
class Artconvector:
    def __init__(self,puth,fontsize = 14,color ="white"):
        self.fontsize = fontsize
        self.color = color
        pygame.init()
        self.puth = puth
        self.image = self.get_image()
        self.res = self.widht,self.height = self.image.shape[0],self.image.shape[1]
        self.screen = pygame.display.set_mode(self.res)
        self.clock = pygame.time.Clock()
        self.ASCII_CHARS = ' .",:!;~+-xmo*#W&8@'
        self.ascii_coef = 255 // (len(self.ASCII_CHARS) - 1)
        self.font = pygame.font.SysFont("Consolas",fontsize,bold=True)
        self.chars_step = int(fontsize * 0.6)             
        self.rendered_chars = [self.font.render(char,False,self.color) for char in self.ASCII_CHARS]
        self.full_text = ""

    def get_image(self):
        self.image_cv2 = cv2.imread(self.puth)
        transform_image = cv2.transpose(self.image_cv2)
        image = cv2.cvtColor(transform_image,cv2.COLOR_BGR2GRAY)
        return image
    def draw_converted_image(self):
        char_includes = self.image // self.ascii_coef
        self.full_text = ""
        for y in range(0,self.height,self.chars_step):
            for x in range(0,self.widht,self.chars_step):
                char_index = char_includes[x,y]
                if char_index:
                    self.full_text += self.ASCII_CHARS[char_index]
                    self.screen.blit(self.rendered_chars[char_index],(x,y))
            self.full_text += "\n"



    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        print(self.full_text)
            self.draw()
            pygame.display.set_caption(str(self.clock.get_fps()))
            pygame.display.flip()
            self.clock.tick()
    def draw(self):
        #pygame.surfarray.blit_array(self.screen,self.image)
        #cv2.imshow("window",self.image_cv2)
        self.screen.fill("black")
        self.draw_converted_image()
if __name__ == "__main__":
    app = Artconvector("snimok.png")
    app.run()

