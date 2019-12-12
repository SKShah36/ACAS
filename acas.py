import argparse
import random


priority = None


class Aircraft:
    def __init__(self, src: tuple=(1, 3), dest: tuple=(2, 3), current_direction=0):
        self._source = src
        self._destination = dest
        self._current_location = [src[0], src[1]]
        self._current_direction = current_direction

    def get_current_location(self):
        return self._current_location

    def get_destination(self):
        return self._destination

    def get_location_data(self) -> tuple:
        x1 = self._current_location[0]
        y1 = self._current_location[1]
        x2 = self._destination[0]
        y2 = self._destination[1]

        return x1, y1, x2, y2, self._current_direction

    def has_reached_destination(self):
        return self._current_location[0] == self._destination[0] and self._current_location[1] == self._destination[1]

    def follow_command(self, command):
        if command == "L":
            self._current_direction = wrap_360(self._current_direction, 90)

        elif command == "R":
            self._current_direction = wrap_360(self._current_direction, -90)

        elif command == "S":
            if self._current_direction == 0:
                self._current_location[0] += 1

            elif self._current_direction == 90:
                self._current_location[1] += 1

            elif self._current_direction == 180:
                self._current_location[0] += -1

            else:
                self._current_location[1] += -1


def wrap_360(current_degrees, rotation_degrees):
    current_degrees += rotation_degrees
    current_degrees = current_degrees % 360

    if current_degrees < 0:
        current_degrees += 360

    return current_degrees


def decide_direction(p, q, direction):
    a = abs(p - q)
    b = abs(p - q) + 1
    c = abs(p - q) - 1

    if b < a:
        return wrap_360(direction, 90), "L"

    elif c < a:
        return wrap_360(direction, -90), "R"


def is_correct_direction(location_data: tuple):
    x1, y1, x2, y2, direction = location_data
    if direction == 0:
        return x1 < x2

    elif direction == 90:
        return y1 < y2

    elif direction == 180:
        return x1 > x2

    elif direction == 270:
        return y1 > y2


def same_coordinates(x1, y1, x2, y2):
    return x1 == x2 and y1 == y2


resolve = False


class AircraftController:
    def __init__(self):
        pass

    def _next_location(self, location_data: tuple):
        x1, y1, x2, y2, direction = location_data

        if direction == 0:
            if x1 < x2:
                x1 += 1
                return x1, y1, direction, "S"
            else:
                if y1 <= y2:
                    return x1, y1, direction, "L"
                else:
                    return x1, y1, direction, "R"

        elif direction == 180:
            if x1 > x2:
                x1 -= 1
                return x1, y1, direction, "S"
            else:
                if y1 <= y2:
                    return x1, y1, direction, "R"
                else:
                    return x1, y1, direction, "L"

        elif direction == 90:
            if y1 < y2:
                y1 += 1
                return x1, y1, direction, "S"
            else:
                if x1 <= x2:
                    return x1, y1, direction, "R"
                else:
                    return x1, y1, direction, "L"

        elif direction == 270:
            if y1 > y2:
                y1 -= 1
                return x1, y1, direction, "S"
            else:
                if x1 <= y2:
                    return x1, y1, direction, "L"
                else:
                    return x1, y1, direction, "R"

    def get_command(self, a1: Aircraft, a2: Aircraft = None):
        global resolve
        if a2 is None:
            location_data = a1.get_location_data()
            command = self._next_location(location_data)[3]
            return command

        else:
            location_data_1 = a1.get_location_data()
            location_data_2 = a2.get_location_data()

            curr_x1, curr_y1, _, _, current_direction_1 = location_data_1
            curr_x2, curr_y2, dest_x2, dest_y2, _ = location_data_2

            new_x1, new_y1, _, _ = self._next_location(location_data_1)
            new_x2, new_y2, _, _ = self._next_location(location_data_2)

            if same_coordinates(new_x1, new_y1, new_x1, new_y2):
                print("Has same coordinates")
                if priority == id(a1):
                    if same_coordinates(new_x1, new_y1, curr_x2, curr_y2):
                        if resolve:
                            resolve = False
                            return "S"
                        else:
                            if curr_y1 == curr_y2:
                                resolve = True
                                if curr_y1 < dest_y2:
                                    return "R"
                                else:
                                    return "L"

                            elif curr_x1 == curr_x2:
                                resolve = True
                                if curr_x1 < dest_x2:
                                    return "L"
                                else:
                                    return "R"

                    else:
                        command = self._next_location(location_data_1)[3]
                        return command

                else:
                    if curr_y1 == curr_y2:
                        if curr_y1 < dest_y2:
                            return "R"
                        else:
                            return "L"

                    elif curr_x1 == curr_x2:
                        resolve = True
                        if curr_x1 < dest_x2:
                            return "L"
                        else:
                            return "R"
            else:
                command = self._next_location(location_data_1)[3]
                return command


def driver(args):
    source1 = (1, 3)
    destination1 = (2, 3)
    source2 = (3, 3)
    destination2 = (2, 3)
    direction1 = 0
    direction2 = 180

    if len(args.source1) == 3:
        source1 = (args.source1[0], args.source1[1])
        direction1 = args.source1[2]

    if len(args.source2) == 3:
        source2 = (args.source2[0], args.source2[1])
        direction2 = args.source2[2]

    if len(args.dest1) == 2:
        source1 = (args.dest1[0], args.dest1[1])

    if len(args.dest2) == 2:
        source1 = (args.dest2[0], args.dest2[1])

    aircraft1 = Aircraft(source1, destination1, direction1)
    controller1 = AircraftController()
    aircraft2 = Aircraft(source2, destination2, direction2)
    controller2 = AircraftController()

    global priority
    priority = random.choice([id(aircraft1), id(aircraft2)])

    if priority == id(aircraft1):
        print("Priority given to first aircraft")

    else:
        print("Priority given to second aircraft")
    while not (aircraft1.has_reached_destination() and aircraft2.has_reached_destination()):
        loc1 = aircraft1.get_location_data()
        loc2 = aircraft2.get_location_data()
        x1, y1, _, _, _ = loc1
        x2, y2, _, _, _ = loc2
        print("Aircraft 1 {}".format(loc1))
        print("Aircraft 2 {}".format(loc2))

        aircraft_distance = abs(x2 - x1) + abs(y2 - y1)

        if aircraft_distance <= 4 and not (aircraft1.has_reached_destination() or aircraft2.has_reached_destination()):
            command1 = controller1.get_command(aircraft1, aircraft2)
            print("Command 1: {}".format(command1))
            command2 = controller1.get_command(aircraft2, aircraft1)
            print("Command 2: {}".format(command2))
            aircraft1.follow_command(command1)
            aircraft2.follow_command(command2)

        elif aircraft1.has_reached_destination():
            command2 = controller2.get_command(aircraft2)
            print("Command 2: {}".format(command2))
            aircraft2.follow_command(command2)

        elif aircraft2.has_reached_destination():
            command1 = controller1.get_command(aircraft1)
            print("Command 1: {}".format(command1))
            aircraft1.follow_command(command1)

        else:
            command1 = controller1.get_command(aircraft1)
            print("Command 1: {}".format(command1))
            command2 = controller2.get_command(aircraft2)
            print("Command 2: {}".format(command2))
            aircraft1.follow_command(command1)
            aircraft2.follow_command(command2)

        if aircraft1.has_reached_destination():
            print("Aircraft1 has reached destination")

        if aircraft2.has_reached_destination():
            print("Aircraft2 has reached destination")

    print("Final locations:")
    print("Aircraft 1 {}".format(aircraft1.get_location_data()))
    print("Aircraft 2 {}".format(aircraft2.get_location_data()))


def main():
    parser = argparse.ArgumentParser(description='Byzantine Fault Tolerance')
    parser.add_argument('-source1', metavar='source1', type=int, nargs='+',
                        help='Please enter the input in the format x y direction:\n where x and y are source '
                             'coordinates '
                             'for aircraft1 and direction is 0 for east, 90 for north, 180 for west and 270 for east')
    parser.add_argument('-source2', metavar='source2', type=int, nargs='+',
                        help='Please enter the input in the format x y direction:\n where x and y are source '
                             'coordinates '
                             'for aircraft2 and direction is 0 for east, 90 for north, 180 for west and 270 for east')
    parser.add_argument('-dest1', metavar='dest1', type=int, nargs='+',
                        help='Please enter the input in the format x y:\n where x and y are destination coordinates '
                             'for aircraft1')
    parser.add_argument('-dest2', metavar='dest2', type=int, nargs='+',
                        help='Please enter the input in the format x y:\n where x and y are destination coordinates '
                             'for aircraft2')

    args = parser.parse_args()
    print(args.source1)
    driver(args)


if __name__ == "__main__":
    main()
