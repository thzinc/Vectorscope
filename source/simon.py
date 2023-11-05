import screennorm
import keyboardcb
import keyleds
import vectoros
import timer
import asyncio
from vos_state import vos_state
import colors
from gc9a01 import color565
import random
import time

GREEN_DK = color565(0x00, 0x66, 0x00)
GREEN_LT = colors.GREEN
RED_DK = color565(0x66, 0x00, 0x00)
RED_LT = colors.RED
YELLOW_DK = color565(0x66, 0x66, 0x00)
YELLOW_LT = colors.YELLOW
BLUE_DK = color565(0x00, 0x00, 0x66)
BLUE_LT = colors.BLUE


screen = screennorm.ScreenNorm()  # get the screen
exit_flag = False  # don't exit


def menu(_):  # menu -bail out
    global exit_flag
    exit_flag = True


activate_state: dict[int, int] = {
    keyleds.KEY_A: 0,
    keyleds.KEY_B: 0,
    keyleds.KEY_C: 0,
    keyleds.KEY_D: 0,
}


def activate(key, dark_only=False, light_only=False):
    args = {}
    activate_color = 0
    deactivate_color = 0
    if key == keyleds.KEY_A:
        args = {"x": 0, "y": 0, "width": 120, "height": 120}
        activate_color = GREEN_LT
        deactivate_color = GREEN_DK

    if key == keyleds.KEY_B:
        args = {"x": 120, "y": 0, "width": 120, "height": 120}
        activate_color = RED_LT
        deactivate_color = RED_DK
    if key == keyleds.KEY_C:
        args = {"x": 0, "y": 120, "width": 120, "height": 120}
        activate_color = YELLOW_LT
        deactivate_color = YELLOW_DK

    if key == keyleds.KEY_D:
        args = {"x": 120, "y": 120, "width": 120, "height": 120}
        activate_color = BLUE_LT
        deactivate_color = BLUE_DK

    def deactivate():
        screen.fill_rect(**args, color=deactivate_color)

    timer.Timer.remove_timer(activate_state[key])
    if dark_only:
        screen.fill_rect(**args, color=deactivate_color)
    elif light_only:
        screen.fill_rect(**args, color=activate_color)
    else:
        screen.fill_rect(**args, color=activate_color)
        activate_state[key] = timer.Timer.add_timer(10, deactivate, True)


allowed_keys = [
    keyleds.KEY_A,
    keyleds.KEY_B,
    keyleds.KEY_C,
    keyleds.KEY_D,
]
expected_keys = []


actual_keys = []


def pad(key):
    global expected_keys, actual_keys
    expected_key = expected_keys[len(actual_keys)]
    activate(key)
    if key == expected_key:
        actual_keys.append(key)
        if len(actual_keys) == len(expected_keys):
            actual_keys = []
            activate(keyleds.KEY_A, light_only=True)
            activate(keyleds.KEY_B, light_only=True)
            activate(keyleds.KEY_C, light_only=True)
            activate(keyleds.KEY_D, light_only=True)
            time.sleep_ms(250)
            activate(keyleds.KEY_A, dark_only=True)
            activate(keyleds.KEY_B, dark_only=True)
            activate(keyleds.KEY_C, dark_only=True)
            activate(keyleds.KEY_D, dark_only=True)
            time.sleep_ms(1500)
            add_key()
    else:
        actual_keys = []
        expected_keys = []
        activate(keyleds.KEY_A, dark_only=True)
        activate(keyleds.KEY_B, dark_only=True)
        activate(keyleds.KEY_C, dark_only=True)
        activate(keyleds.KEY_D, dark_only=True)
        time.sleep_ms(1500)
        add_key()


def add_key():
    global expected_keys
    new = random.choice(allowed_keys)

    expected_keys.append(new)
    activate(new)


async def vos_main():
    global exit_flag, expected_keys, actual_keys
    # we treat the joystick like any other key here
    keys = keyboardcb.KeyboardCB(
        {
            keyleds.KEY_MENU: menu,
            keyleds.KEY_A: pad,
            keyleds.KEY_B: pad,
            keyleds.KEY_C: pad,
            keyleds.KEY_D: pad,
        }
    )

    activate(keyleds.KEY_A, dark_only=True)
    activate(keyleds.KEY_B, dark_only=True)
    activate(keyleds.KEY_C, dark_only=True)
    activate(keyleds.KEY_D, dark_only=True)
    expected_keys = []
    actual_keys = []
    add_key()

    # do nothing... everything is on keyboard and timer
    while exit_flag == False:
        await asyncio.sleep_ms(500)
    # stop listening for keys
    keys.detach()
    # timer.Timer.remove_timer(tid)
    for key in activate_state:
        timer.Timer.remove_timer(activate_state[key])
    exit_flag = False  # next time

    vos_state.show_menu = True  # tell menu to wake up


if __name__ == "__main__":
    import vectoros

    vectoros.run()
