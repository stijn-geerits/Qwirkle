from operator import abs
from math import atan2, degrees, pi


class Line:
    def __init__(self, start_position, end_position):
        self.start_position = start_position
        self.end_position = end_position
        self.length = 0
        self.angle = 0

    def get_start_position(self):
        return self.start_position

    def get_end_position(self):
        return self.end_position

    def get_length(self):
        """
        Calculate the length of the line and return the result
        """
        distance_vector = (self.start_position[0] - self.end_position[0], self.start_position[1] - self.end_position[1])
        self.length = sum(tuple(map(abs, distance_vector))) + 1

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

        angle_radian = atan2(dy, dx)  # Might have to reverse dy to account for flipped axes in pygame
        self.angle = degrees(angle_radian % 2*pi)  # Convert to degrees

        return self.angle


# Test
if __name__ == '__main__':
    line = Line((1, 6), (1, 2))
    line_length = line.get_length()
    print("The length of the line is: " + str(line_length))
    line_angle = line.get_angle()
    print("The angle of the line is: " + str(line_angle))
