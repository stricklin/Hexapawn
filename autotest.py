import sys
import os
import time
import Hexapawn


def test_positions(directory):
    files = os.listdir(directory)
    files.sort()
    input_files = []
    output_files = []
    for file in files:
        if file.count(".in") > 0:
            input_files.append(file)
        else:
            output_files.append(file)
    for test in range(len(input_files)):
        start_time = time.time()
        output = int(open(directory + '/' + output_files[test]).read())
        hexapawn_input = open(directory + '/' + input_files[test]).read().splitlines()
        hexapawn = Hexapawn.Hexapawn(hexapawn_input)
        assert output == hexapawn.position_value(logging=True)
        end_time = time.time()
        sys.stderr.write(output_files[test] + "\n")
        sys.stderr.write(str(end_time - start_time) + "\n")

if __name__ == "__main__":
    test_positions("positions")
