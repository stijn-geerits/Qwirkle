import math
# TODO: method to check two lines to see if they are equivalent, keep in mind false equivalencies (min of x and y)


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


# Test
if __name__ == '__main__':
    line = Line((1, 2), (1, 6))
    line_length = line.get_length()
    print("The length of the line is: " + str(line_length))
    line_angle = line.get_angle()
    print("The angle of the line is: " + str(line_angle))
