import pygame 
from loguru import logger
from numba import njit
import numpy
import cv2
class Artconvector:
    def __init__(self,puth,fontsize = 14,colorlevel=8):
        self.fontsize = fontsize
        self.colorlevel = colorlevel
        pygame.init()
        self.puth = puth
        self.grayimage,self.rgbimage = self.get_image()
        self.res = self.widht,self.height = self.grayimage.shape[0],self.grayimage.shape[1]
        self.screen = pygame.display.set_mode(self.res)
        self.clock = pygame.time.Clock()
        self.ASCII_CHARS = ' ixzao*MW&8%B@$#'
        self.ascii_coef = 255 // (len(self.ASCII_CHARS) - 1)
        self.font = pygame.font.SysFont("Consolas",fontsize,bold=True)
        self.chars_step = int(fontsize * 0.6)
        #self.rendered_chars = [self.font.render(char,False,"white") for char in self.ASCII_CHARS]
        self.pallet,self.colorcf =  self.create_palet()
        self.full_text = ""
    def create_palet(self):
        colors,colorcf = numpy.linspace(0,255,num=self.colorlevel,dtype=int,retstep=True)
        colorpalet = [numpy.array([r,g,b])for r in colors for g in colors for b in colors]
        palet = dict.fromkeys(self.ASCII_CHARS,None)
        colorcf = int(colorcf)
        for char in palet:
            char_palet = {}
            for color in colorpalet:
                colorkey = tuple(color // colorcf)
                char_palet[colorkey] = self.font.render(char,False,tuple(color))
            palet[char] = char_palet
        return palet,colorcf
    

    def get_image(self):
        self.image_cv2 = cv2.imread(self.puth)
        transform_image = cv2.transpose(self.image_cv2)
        grayimage = cv2.cvtColor(transform_image,cv2.COLOR_BGR2GRAY)
        rgbimage = cv2.cvtColor(transform_image,cv2.COLOR_BGR2RGB)
        return grayimage, rgbimage
    def draw_converted_image(self):
        char_includes = self.grayimage // self.ascii_coef
        colorincludes = self.rgbimage // self.colorcf
        self.full_text = ""
        for y in range(0,self.height,self.chars_step):
            for x in range(0,self.widht,self.chars_step):
                char_index = char_includes[x,y]
                if char_index:
                    self.full_text += self.ASCII_CHARS[char_index]
                    char = self.ASCII_CHARS[char_index]
                    color = tuple(colorincludes[x,y])
                    self.screen.blit(self.pallet[char][color],(x,y))
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
    app = Artconvector("kartinka.png")
    app.run()

