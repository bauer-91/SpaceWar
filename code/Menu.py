import pygame.image

class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/menu.jpg')
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self, ):
        pygame.mixer.music.load('./asset/menu.wav')
        pygame.mixer.music.play(-1)
        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            pygame.display.flip()
            # Check for all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Close Window
                    quit()  # End pygame