start_positions = [(242, 0, 45), (308, -7, 25)]  #
cubes_position = [(20, 220, -40), (-30, 220, -40), (-60, 220, -40)]
cubes = [0, 0, 0]
color = [1, 1, 1]

speed_rail = [10400, 5500, 3666]

delta = 30  # the deviation value for the next cube

__cubes_max_value__ = int((320 - cubes_position[0][1]) / delta) + 1  # max value of dobot is 320,

cubes_value = 12  # there you indicate how many cubes you need to sort


if cubes_value > __cubes_max_value__ * 3:
    print("Dobot could put {0} in a row\n"
          "You should make 'cubes_value' < {1} or change start_coordinates"
          .format(__cubes_max_value__, __cubes_max_value__))
    quit()

file_color = open(r"D:\PythonProjects\Two_Dobots_1\color.py", "w+")
# config file, where status of first dobot is indicated
file_color.write("[1, 1, 1]w1")  # the standard of communication, where [0,0,1] - color, w0 or w1 - status of first
file_color.close()     # when "w1" second dobot could work => when DOBOT1 wait for cube, DOBOT2 could work
dType.SetIOMultiplexingEx(api, 5, 1, 1)  # init port to voltage 3.3
dType.SetIODOEx(api, 5, 1, 1)  # init port as color sensor
dType.SetColorSensor(api, 1, 3, 1)  # init color sensor

dType.SetPTPCmdEx(api, 0, start_positions[0][0], start_positions[0][1], start_positions[0][2], 0, 1)

for cube in range(cubes_value):
    dType.SetInfraredSensor(api, 1, 1, 0)  # init infrared sensor
    dType.SetEMotorEx(api, 0, 1, 2000, 1)  # start rail to make it parallel with robot

    # go to position of cube
    while (dType.GetInfraredSensor(api, 1)[0]) == 0:  # waiting for cube in sensor
        dType.SetEMotorEx(api, 0, 1, speed_rail[color.index(1)], 1)
    print('Found cube')
    dType.dSleep(300 * (color.index(1)+1))
    print('Cube delivered')
    dType.SetEMotorEx(api, 0, 0, 0, 1)  # turn off rail
    dType.SetInfraredSensor(api, 0, 1, 0)  # turn off infrared sensor
    print('Wait for robot')
    dType.SetEndEffectorParamsEx(api, 59.7, 0, 0, 1)  # init compressor
    dType.SetEndEffectorSuctionCupEx(api, 1, 1)  # turn on compressor
    dType.SetPTPCmdEx(api, 7, 0, 0, (-35), 0, 1)  # capture cube
    dType.dSleep(100)
    dType.SetPTPCmdEx(api, 0, start_positions[1][0], start_positions[1][1], start_positions[1][2], 0,
                      1)  # carry to color sensor
    dType.SetEMotorEx(api, 0, 1, 1000, 1)  # turn on the rail very slow to make some kind of threading

    R, G, B = 0, 0, 0  # start values
    color = [0, 0, 0]  # color of cube in RGB ([R, G, B])
    for i in range(5):  # cycle to more accurate reading of color
        R += dType.GetColorSensorEx(api, 0)  # if color RED, R +=1
        G += dType.GetColorSensorEx(api, 1)  # if color GREEN, G +=1
        B += dType.GetColorSensorEx(api, 2)  # if color BLUE, B +=1
        dType.dSleep(50)  # delay for clearing noise
    print(R, G, B)  # in the end of cycle, we get (5, 0, 0) or (0, 5, 0) or (0, 0, 5)
    print("___")
    chance = max(R, G, B)

    if chance == R:
        color = [1, 0, 0]
    elif chance == G:
        color = [0, 1, 0]
    else:
        color = [0, 0, 1]

    file_color = open(r"D:\PythonProjects\Two_Dobots_1\color.py", "w+")
    file_color.write(str(color)+"w0")
    file_color.close()

    # when DOBOT1 get cube and its color, DOBOT2 musn't move!;

    print("color = ", color)  # getting color as [0, 1, 0] or ect.
    #  there, color is equal to position if GREEN == 1([0, 1, 0]) => position == [0, 1, 0]
    dType.SetPTPCmdEx(api, 0, -30, 220, -40, 0, 1)
    dType.SetEndEffectorSuctionCupEx(api, 0, 1)  # turn off the compressor

    for i in range(3):
        cubes[i] += color[i]
        # there we understand how many cubes in each place ( on second value there will be [0, 2, 0])
    print("cubes = ", cubes)


    dType.SetPTPCommonParamsEx(api, 500, 75, 1)
    current_pose = dType.GetPose(api)
    dType.SetPTPCmdEx(api, 2, 115, 220, 45, current_pose[3], 1)

    file_color = open(r"D:\PythonProjects\Two_Dobots_1\color.py", "w+")
    file_color.write(str(color) + "w1")
    file_color.close()

    current_pose = dType.GetPose(api)
    dType.SetPTPCmdEx(api, 2, start_positions[0][0], start_positions[0][1], start_positions[0][2], current_pose[3], 1)

    #dType.SetPTPCmdEx(api, 0,  0, 1)

# after cycle back home
dType.SetPTPCmdEx(api, 0, start_positions[0][0], start_positions[0][1], start_positions[0][2], 0, 1)
dType.SetEMotorEx(api, 0, 0, 0, 1)  # turn off rail
dType.SetHOMECmdEx(api, 0, 1)
