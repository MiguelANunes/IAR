import FileHandler

def main():

    simulationMap = FileHandler.load_map()
    robot         = FileHandler.generate_robot(simulationMap, True)
    itemList      = FileHandler.generate_items(simulationMap, robotPos=robot.position)
    factoryList   = FileHandler.generate_factories(simulationMap, robotPos=robot.position)

    if simulationMap == None:
        exit()

    factoryPositions = [(f.tipo, f.position) for f in factoryList]
    itemPosition     = [(i.tipo, i.position) for i in itemList]

    FileHandler.dump_robot(robot.position)
    FileHandler.dump_factories(factoryPositions)
    FileHandler.dump_items(itemPosition)


if __name__ == "__main__":
    main()