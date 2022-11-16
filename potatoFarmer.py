from wizAPI import *
import math
player = wizAPI().register_window()


def print_separator(*args):
    sides = '+'*16
    _str = " ".join([sides, " ".join(args), sides])
    l = len(_str)
    print('='*l)
    print(_str)
    print('='*l)


def print_time(timer):
    minutes = math.floor(timer/60)
    seconds = math.floor(timer % 60)

    if minutes == 0:
        print('Round completed in {} seconds.'.format(seconds))
    else:
        print('Round completed in {} minutes and {} seconds.'.format(minutes, seconds))


ROUND_COUNT = 0
while True:
    ROUND_COUNT += 1
    START_TIME = time.time()
    print_separator('ROUND', str(ROUND_COUNT))

    """ Check if we need to use a potion """
    player.use_potion_if_needed()

    """ Try to get in battle """
    while player.is_idle():
        (
            player.hold_key('w', 1)
            .hold_key('s', 1)
        )

    print(""" Success! now wait for our turn to play """)
    player.wait_for_turn_to_play()

    while (not player.is_idle()) and (player.count_enemies() < 2):
        print('Waiting for more enemies to join')
        if player.find_spell('empower'):
            player.cast_spell('empower')
        (player.wait(5)
         .pass_turn())


        player.wait_for_end_of_round()

    inFight = not player.is_idle()
    while inFight:
        if player.enchant('scarecrow', 'accurate') or player.find_spell('scarecrow-enchanted'):
            player.cast_spell('scarecrow-enchanted')
        elif player.find_spell('empower'):
            player.cast_spell('empower')
        else:
            player.pass_turn()

        player.wait_for_end_of_round()

        if player.is_idle():
            inFight = False

    print_time(time.time() - START_TIME)

# Fight complete!
