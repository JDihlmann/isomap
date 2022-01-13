import sys
from RegionTimeDistanceMapper.regionTimeDistanceMapper import RegionTimeDistanceMapper

"""
Main File
Description:
Loads arguments from command line and starts up application.
"""

def main(argv):
    #  TODO: Give arguments such as origin, radius, gridSize, etc.

    #if len(argv) != 1:
        # print('test.py <inputimage>')
        # sys.exit(2)


    regionTimeDistanceMapper = RegionTimeDistanceMapper(
        origin="Tübingen Rathaus",
        bounds=(10, 10),
        gridSize=(10, 10)
    )

    # regionTimeDistanceMapper.getTimeDistanceFor(TransportationType.Foot)

if __name__ == "__main__":
    main(sys.argv[1:])