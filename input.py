from pyfirmata import Arduino, util

board = Arduino('COM5')

it = util.Iterator(board)
it.start()

analog_0 = board.get_pin('a:0:i')


def run_neuro_cycle():
    value = float(analog_0.read())

    return value
