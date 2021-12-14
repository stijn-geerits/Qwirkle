import math


class Line:
    def __init__(self, start_position, end_position):
        self.start_position = start_position
        self.end_position = end_position
        self.length = self.get_length()
        self.angle = self.get_angle()

    def get_start_position(self):
        return self.start_position

    def get_end_position(self):
        return self.end_position

    def get_length(self):
        """
        Calculate the length of the line and return the result
        """
        self.length = math.dist(self.start_position, self.end_position) + 1  # + 1 to account for starting tile

        return self.length

    def get_angle(self):
        """
        Calculate the angle of the line and return the result.\n
        0 degrees: The endpoint is to the right of the starting point.\n
        90 degrees: The endpoint is above the starting point.\n
        180 degrees: The endpoint is to the left of the starting point.\n
        270 degrees: The endpoint is below the starting point.
        """
        dx = self.end_position[0] - self.start_position[0]
        dy = self.end_position[1] - self.start_position[1]

        angle_radian = math.atan2(-dy, dx)  # Reverse dy to account for flipped axes in pygame
        angle_radian %= 2*math.pi
        self.angle = math.degrees(angle_radian)  # Convert to degrees

        return self.angle

    def is_equal(self, other_line):
        """
        Checks if this line object is equal to another by comparing the start and end position of
        this line and the other. Returns True if lines are equal.
        """
        # If one line is vertical and the other horizontal, they can't be equal
        angle_difference = abs(self.angle - other_line.get_angle())
        if angle_difference % 180 != 0:
            return False

        # Check if lines constitute the same positions
        other_line_sp = other_line.get_start_position()
        other_line_ep = other_line.get_end_position()

        other_line_attr = [other_line_sp, other_line_ep]
        attr = [self.start_position, self.end_position]

        other_line_attr.sort()
        attr.sort()

        if other_line_attr == attr:
            return True
        else:
            return False
