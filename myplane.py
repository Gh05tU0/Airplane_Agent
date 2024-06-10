import pygame

GRID_SIZE = 50  # 定义网格大小

class MyPlane(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load("images/me1.png").convert_alpha()
        self.image2 = pygame.image.load("images/me2.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load("images/me_destroy_1.png").convert_alpha(), \
            pygame.image.load("images/me_destroy_2.png").convert_alpha(), \
            pygame.image.load("images/me_destroy_3.png").convert_alpha(), \
            pygame.image.load("images/me_destroy_4.png").convert_alpha() \
            ])
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = \
            (self.width - self.rect.width) // 2, \
            self.height - self.rect.height - 60
        self.active = True
        self.invincible = False
        self.mask = pygame.mask.from_surface(self.image1)

    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= GRID_SIZE
            self.rect.top = max(0, self.rect.top)

    def moveDown(self):
        if self.rect.bottom < self.height:
            self.rect.top += GRID_SIZE
            self.rect.top = min(self.height - self.rect.height, self.rect.top)

    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= GRID_SIZE
            self.rect.left = max(0, self.rect.left)

    def moveRight(self):
        if self.rect.right < self.width:
            self.rect.left += GRID_SIZE
            self.rect.left = min(self.width - self.rect.width, self.rect.left)

    def reset(self):
        self.rect.left, self.rect.top = \
            (self.width - self.rect.width) // 2, \
            self.height - self.rect.height - 60
        self.active = True
        self.invincible = True
