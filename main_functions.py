import time
from pydobot import Dobot


def read_file(path: str = r"D:\PythonProjects\Two_Dobots_1\color.py"):
    w = "0"  # the state of readiness of first dobot.
    # When wait == "0" second dobot can not work, when wait == "1" second dobot can work
    col = "[1, 1, 1]"  # default value of color. First DOBOT gives same information, until it got color

    while col == "[1, 1, 1]" or w == "0":  # while we don't know the color, we read file
        file = open(path, "r")
        line = str(file.read())
        col, w = line.split("w")
        time.sleep(0.5)

    col = [int(ch) for ch in list((((col.replace(' ', '')).replace('[', '')).replace(']', '')).replace(',', ''))]

    print(col)
    return col, w


def write_file(condition: str = "[1, 1, 1]w0"):
    file = open(r"D:\PythonProjects\Two_Dobots_1\color.py", "w+")
    file.write(condition)  # write to file to prevent gripping the same cube
    file.close()


def go_to_position(dobot: Dobot, coordinates: tuple = None, delta: int = 0, distance: int = None, suck: bool = False):
    time_list = [3.4, 6, 8.9]  # list of time for each position

    dobot.suck(suck)  # turn on/off sucker

    if not coordinates and delta:  # if we need only descend, save x, y constant
        x, y, z, r = dobot.get_pose().position  # getting pose of dobot, to have x, y, z
        dobot.move_to(x, y, z - delta)
    else:
        dobot.move_to(coordinates[0], coordinates[1], coordinates[2])  # move to coordinates
        time.sleep(0.3)
        dobot.move_to(coordinates[0], coordinates[1], coordinates[2] - delta, coordinates[3])  # move to coordinates
    time.sleep(0.5)  # some time to finish movement

    if suck and delta:
        time.sleep(1.2)  # some time to finish sucking

    if distance:  # turn on rail on distance
        dobot.conveyor_belt_distance(speed=26.5, distance=abs(distance), direction=(distance / abs(distance)))
        # turn on rail on speed = 27, distance = distance of color, direction = 1 or -1
        time.sleep(time_list[cube_to_position.index(abs(distance))])  # some time to finish movement of rail


if __name__ == "__main__":
    device = Dobot(port="COM4")  # init DOBOT (always check COM port)
    cubes = [0, 0, 0]  # init list of all cubes to understand how many cubes of each color

    #   _positions = [(position with cube), (start position to make it faster)]
    main_positions = [(200, 0, -45, 0), (-150, -240, 55, 0)]  # start positions

    cube_on_position = (-5, -232, -45, 0)  # start cubes position

    cube_to_position = [20000, 40000, 60000]  # rail positions [red, green, blue]

    for _ in range(12):
        go_to_position(device, main_positions[1])  # moving to start position (вышли на исходную)

        color, wait = read_file()  # waiting cube (ждем подтверждение из файла)
        go_to_position(device,
                       coordinates=cube_on_position, delta=80,  # descend behind the cube (забираем кубик)
                       suck=True)  # with sucker turned on

        go_to_position(device,
                       main_positions[0],  # moving up
                       distance=cube_to_position[color.index(1)],  # moving rail to position of color cube
                       suck=True)  # забираем кубик и едем на позицию кубика определенного цвета
        write_file(str(color) + "w0")  # write to file, that cube is gone (запись в файл, что кубик был поднят)

        coordinates_cube = (main_positions[0][0] + (50 if color[1] == 1 else 0),
                            main_positions[0][1] + 30 * cubes[color.index(1)],
                            main_positions[0][2],
                            0 - 20 * cubes[color.index(1)])

        go_to_position(device,
                       coordinates=coordinates_cube,
                       delta=60,  # descend to put the cube (отвезли кубик на дистанцию, теперь опускаем кубик)
                       suck=True)
        go_to_position(device, main_positions[1],  # back to min position,
                       distance=-cube_to_position[color.index(1)],  # start rail in direction of 0
                       suck=False)  # turn off sucker, (отключаем компрессор, поднимаемся на необходимую высоту и рельсу

        for i, c in enumerate(color):
            cubes[i] += c

    device.home()
