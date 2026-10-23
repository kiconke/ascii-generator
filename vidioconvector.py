import pygame 
from loguru import logger
from numba import njit
import numpy
import cv2
class Artconvector:
    def __init__(self,puth,fontsize = 10,colorlevel=8):
        self.capchur = cv2.VideoCapture(puth)
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
        self.fpsrecord = 30
        self.record = True
        self.recorder = cv2.VideoWriter("output.mp4",cv2.VideoWriter_fourcc(*"mp4v"),self.fpsrecord,self.res)
    def record_frame(self):
        if self.record:
            frame = self.getframe()
            self.recorder.write(frame)
            cv2.imshow("frame",frame)
            
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
        #self.image_cv2 = cv2.imread(self.puth)
        okay,self.image_cv2 = self.capchur.read()
        if not okay:
            exit()

        transform_image = cv2.transpose(self.image_cv2)
        grayimage = cv2.cvtColor(transform_image,cv2.COLOR_BGR2GRAY)
        rgbimage = cv2.cvtColor(transform_image,cv2.COLOR_BGR2RGB)
        return grayimage, rgbimage
    def draw_converted_image(self):
        self.grayimage,self.rgbimage = self.get_image()
        char_includes = self.grayimage // self.ascii_coef
        colorincludes = self.rgbimage // self.colorcf
        
        values = convert(self.rgbimage,self.grayimage,self.widht,self.height,self.colorcf,self.ascii_coef,self.chars_step)
        for char_index,color,pos in values:      
            char = self.ASCII_CHARS[char_index]
            self.screen.blit(self.pallet[char][color],pos)



    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.record = not self.record
                    if event.key == pygame.K_ESCAPE and self.record == True:
                        self.record = not self.record
                        cv2.destroyAllWindows()

            self.draw()
            self.record_frame()
            pygame.display.set_caption(str(self.clock.get_fps()))
            pygame.display.flip()
            self.clock.tick(30)
    def draw(self):
        #pygame.surfarray.blit_array(self.screen,self.image)
        #cv2.imshow("window",self.image_cv2)
        self.screen.fill("black")
        self.draw_converted_image()
    def getframe(self):
        frame = pygame.surfarray.array3d(self.screen)
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        frame = cv2.transpose(frame)
        return frame
@njit
def convert(image,imagegray,widgh,hight,colorcoef,ascii_coef,step):
    value = []
    for x in range(0,widgh,step):
        for y in range(0,hight,step):
            char_index = imagegray[x,y] // ascii_coef
            if char_index:
                r,g,b = image[x,y] // colorcoef
                value.append((char_index,(r,g,b),(x,y)))
    return value
if __name__ == "__main__":
    app = Artconvector("vid.mp4")
    app.run()

