"""Abstraction of a visualization movement (sub-visulization or visualization state).

Abstraction of a visualization movement (sub-visulization or visualization state) in which there are
collection of visualizations shown at the same time.

License: BSD
"""


class VizMovement:
    """Interface for a visualization movement."""

    def check_state(self, mouse_x: float, mouse_y: float):
        """Check if the state of the visualization should be updated.

        Args:
            mouse_x: The x coordinate of the cursor or last touchscreen input.
            mouse_y: The y coordinate of the cursor or last touchscreen input.
        """
        raise RuntimeError('Use implementor.')

    def draw(self):
        """Re-draw this sub-visualization / visualization state."""
        raise RuntimeError('Use implementor.')

    def refresh_data(self):
        """Update the dataset within this sub-visualization."""
        raise RuntimeError('Use implementor.')

    def on_change_to(self):
        """Method to call when the visualization is about to swtich to this movement."""
        pass
