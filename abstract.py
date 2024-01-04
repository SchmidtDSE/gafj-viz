class VizMovement:

    def check_hover(self, mouse_x: float, mouse_y: float):
        raise RuntimeError('Use implementor.')

    def draw(self):
        raise RuntimeError('Use implementor.')

    def refresh_data(self):
        raise RuntimeError('Use implementor.')
