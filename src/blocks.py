import copy
import random
import pygame
import numpy as np
from constants import *
from exceptions import *


class Block(pygame.sprite.Sprite):

    @staticmethod
    def collide(block, group):
        """
        Check if the specified block collides with some other block in the group.
        """
        for other_block in group:
            # Ignore the current block which will always collide with itself
            if block == other_block:
                continue
            if pygame.sprite.collide_mask(block, other_block) is not None:
                return True
        return False

    def __init__(self):
        super().__init__()
        self.superposed = None
        self.current = True
        self.struct = np.array(self.struct)
        # Initial random rotation
        if random.randint(0, 1):
            self.struct = np.rot90(self.struct)
        self._draw()

    def _draw(self, x=5, y=0):
        width = len(self.struct[0]) * TILE_SIZE
        height = len(self.struct) * TILE_SIZE
        small_width = len(self.struct[0]) * SMALL_TILE_SIZE
        small_height = len(self.struct) * SMALL_TILE_SIZE
        self.image = pygame.surface.Surface([width, height])
        self.image.set_colorkey((0, 0, 0))
        # Small image for upcoming blocks
        self.small_image = pygame.surface.Surface([small_width, small_height])
        self.small_image.set_colorkey((0, 0, 0))
        # Position and size
        self.rect = pygame.Rect(0, 0, width, height)
        self.x = x
        self.y = y
        for y, row in enumerate(self.struct):
            for x, col in enumerate(row):
                if col:
                    pygame.draw.rect(self.image, self.color,
                                     pygame.Rect(x * TILE_SIZE + 1, y * TILE_SIZE + 1,
                                                 TILE_SIZE - 2, TILE_SIZE - 2))
                    pygame.draw.rect(self.small_image, self.color,
                                     pygame.Rect(x * SMALL_TILE_SIZE + 1, y * SMALL_TILE_SIZE + 1,
                                                 SMALL_TILE_SIZE - 2, SMALL_TILE_SIZE - 2))
        self._create_mask()

    def redraw(self):
        self._draw(self.x, self.y)

    def _create_mask(self):
        """
        Create the mask attribute from the main surface.
        The mask is required to check collisions. This should be called after the surface is created or update.
        """
        self.mask = pygame.mask.from_surface(self.image)

    def initial_draw(self):
        raise NotImplementedError

    @property
    def group(self):
        return self.groups()[0]

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.rect.left = value * TILE_SIZE

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.rect.top = value * TILE_SIZE

    def move_left(self, group):
        self.x -= 1
        # Check if we reached the left margin
        if self.x < 0 or Block.collide(self, group):
            self.x += 1

    def move_right(self, group):
        self.x += 1
        # Check if we reached the right margin or collided with another block
        if self.rect.right > GRID_WIDTH or Block.collide(self, group):
            # Rollback
            self.x -= 1

    def move_down(self, group):
        self.y += 1
        # Check if the block reached the bottom or collided with another one
        if self.rect.bottom > GRID_HEIGHT or Block.collide(self, group):
            # Rollback to the previous position
            self.y -= 1
            self.current = False
            raise BottomReached

    def rotate(self, group):
        self.image = pygame.transform.rotate(self.image, 90)
        # Once rotated we need to update the size and position
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()
        self._create_mask()
        # Check the new position doesn't exceed the limits or collide with other blocks
        # and adjust it if necessary
        while self.rect.right > GRID_WIDTH:
            self.x -= 1
        while self.rect.left < 0:
            self.x += 1
        while self.rect.bottom > GRID_HEIGHT:
            self.y -= 1
        while True:
            if not Block.collide(self, group):
                break
            self.y -= 1
        self.struct = np.rot90(self.struct)


class SquareBlock(Block):
    struct = (
        (1, 1),
        (1, 1)
    )
    color_100 = (92, 142, 38)
    color_50 = (146, 208, 80)
    color_25 = (196, 229, 159)
    color = color_100


class TBlock(Block):
    struct = (
        (1, 1, 1),
        (0, 1, 0)
    )
    color_100 = (255, 51, 204)
    color_50 = (255, 139, 225)
    color_25 = (255, 205, 242)
    color = color_100


class LineBlock(Block):
    struct = (
        (1,),
        (1,),
        (1,),
        (1,)
    )
    color_100 = (0, 176, 240)
    color_50 = (101, 215, 255)
    color_25 = (179, 235, 235)
    color = color_100


class LBlock(Block):
    struct = (
        (1, 1),
        (1, 0),
        (1, 0),
    )
    color_100 = (112, 48, 160)
    color_50 = (165, 104, 210)
    color_25 = (205, 172, 230)
    color = color_100


class LIBlock(Block):
    struct = (
        (1, 1),
        (0, 1),
        (0, 1),
    )
    color_100 = (238, 138, 18)
    color_50 = (245, 186, 115)
    color_25 = (250, 222, 188)
    color = color_100


class ZBlock(Block):
    struct = (
        (0, 1),
        (1, 1),
        (1, 0),
    )
    color_100 = (172, 0, 0)
    color_50 = (255, 0, 0)
    color_25 = (255, 113, 113)
    color = color_100


class ZIBlock(Block):
    struct = (
        (1, 0),
        (1, 1),
        (0, 1),
    )
    color_100 = (0, 81, 242)
    color_50 = (91, 146, 255)
    color_25 = (171, 199, 255)
    color = color_100

# TODO: poner este codigo en un archivo separado
class QuantumBlock:
    """
    It stores a superposed block, and keeps the record of the blocks that were generated from
    the original (which was at 100%), it can save up to 4 sub-blocks, the possible configurations are:
       [ block at 50% , block at 50%, None,         None ]
       [ block at 50% , block at 25%, block at 25%, None ]
       [ block at 25% , block at 25%, block at 25%, block at 25% ]
    """

    types_blocks = {
        'SquareBlock': SquareBlock,
        'TBlock': TBlock,
        'LineBlock': LineBlock,
        'LBlock': LBlock,
        'LIBlock': LIBlock,
        'ZBlock': ZBlock,
        'ZIBlock': ZIBlock
    }

    def __init__(self, original_block, group):
        # When a set of superposed blocks is created for the first time, we will always be in the
        # case of having two parts, with 50%/50%

        block_left = self._create_superposed_block(self, original_block)          # tile left
        block_right = self._create_superposed_block(self, original_block, False)  # tile right

        block_right.current = True

        # Check that the positions doesn't exceed the limits or collide with other blocks
        # and adjust it if necessary
        while block_right.rect.right > GRID_WIDTH:
            block_left.x -= 1
            block_right.x -= 1
        while block_left.rect.left < 0:
            block_left.x += 1
            block_right.x += 1
        while block_left.rect.bottom > GRID_HEIGHT:
            block_left.y -= 1
        while block_right.rect.bottom > GRID_HEIGHT:
            block_right.y -= 1
        while True:
            if not Block.collide(block_left, group):
                break
            block_left.y -= 1
        while True:
            if not Block.collide(block_right, group):
                break
            block_right.y -= 1

        # The blocks are added in the order of creation, that is, in the sprite list,
        # the last block created is up to the "top"
        self.set_blocks = [block_left, block_right, None, None]
        #self.bottom_reach = [False, False, True, True]

    @staticmethod
    def _create_superposed_block(qb, original_block, left=True):
        block = QuantumBlock.types_blocks[type(original_block).__name__]()
        block.color = block.color_50
        block.struct = original_block.struct
        block.current = False
        block.y = original_block.y
        width_block = len(original_block.struct[0])
        block.x = original_block.x + int(width_block / 2) + (-width_block if left else 1)
        block.superposed = qb
        block.bottom_reach = False
        block.redraw()

        return block
