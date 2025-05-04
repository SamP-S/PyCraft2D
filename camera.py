from core import *

# TODO register all cameras in state
# TODO allow swapping between cameras using an active camera flag

class Camera:
    
    PPS = 32    # pixel per square
    
    def __init__(self, target:Entity | None = None):
        """Initialise the camera."""
        # view controls
        self.zoom: float = 1.0
        self.target: Entity | None = target
        
    def world_to_screen(self, wx:float, wy:float) -> tuple[float, float]:
        """Convert world coordinates to screen coordinates."""
        assert(self.zoom > 0)
        # get viewport size
        w, h = pg.display.get_surface().get_size()
        # get target position
        tx, ty = (0, 0)
        if self.target is not None:
            tx, ty = self.target.x, self.target.y
        
        # calc delta to target
        dx = wx - tx
        dy = wy - ty
        # adjust delta for zoom
        dx = dx * self.zoom * Camera.PPS
        dy = dy * self.zoom * Camera.PPS
        # calc coordinates
        x = (w // 2) + dx
        y = (h // 2) + dy
        # switch y-axis direction
        sx = x
        sy = h - y
        return (sx, sy)
    
    def screen_to_world(self, sx:float, sy:float) -> tuple[float, float]:
        """Convert screen coordinates to world coordinates."""
        assert(self.zoom > 0)
        # get viewport size
        w, h = pg.display.get_surface().get_size()
        # get target position
        tx, ty = (0, 0)
        if self.target is not None:
            tx, ty = self.target.x, self.target.y
            
        # switch y-axis direction
        x = sx
        y = h - sy
        # calc delta to target
        dx = x - (w / 2)
        dy = y - (h / 2)
        # adjust delta for zoom
        dx = dx / (self.zoom * Camera.PPS)
        dy = dy / (self.zoom * Camera.PPS)
        # calc world coordinates
        wx = tx + dx
        wy = ty + dy
        return (wx, wy)
    
if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((800, 600))
    camera = Camera()
    print(camera.world_to_screen(0, 0))
    print(camera.screen_to_world(400, 300))
    print(camera.world_to_screen(1, 1))
    print(camera.screen_to_world(1, 1))
    pg.quit()