import argparse

from main import run, CorruptedDataException, WrongTimeException


def _get_input(inputs):
    input_name = ""
    input = []
    for line in inputs:
        if line[:6] == "INPUT:":
            if input:
                yield input_name, input
            input_name = line[7:]
            input = []
        else:
            input.append(line)
    if input:
        yield input_name, input


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        default="MULTIPLE_INPUTS",
        help='input file name e.g. "MULTIPLE_INPUT"',
    )
    parser.add_argument(
        "-o",
        "--output",
        default="MULTIPLE_OUTPUTS",
        help='output file name e.g. "MULTIPLE_OUTPUT"',
    )
    args = parser.parse_args()
    input_filename = args.input
    output_filename = args.output
    try:
        inputs = open(f"{input_filename}.txt", "r")
        print(f"Started. Input file: {inputs.name}")
    except:
        raise

    open(f"{output_filename}.txt", "w").close()
    with open(f"{output_filename}.txt", "a") as output:
        line_n = 0
        for input_name, input in _get_input(inputs):
            line_n += 1
            output.write(input_name)
            try:
                for line in run(input):
                    line_n += 1
                    output.write(f"{line[0]}-{line[1]}: {line[2]}\n")
            except WrongTimeException as e:
                raise WrongTimeException(line_n + e.line_n, e.line)
            except CorruptedDataException as e:
                raise CorruptedDataException(line_n + e.line_n, e.line)
    print(f"Finished. Output file: {output_filename}.txt")
