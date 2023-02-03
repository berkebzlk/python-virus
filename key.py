from pynput.keyboard import Listener

the_keys = []
a = 0


def runkey(name, z=20):
    global x
    x = z

    with Listener(
            on_press=functionPerKey,
            on_release=onEachKeyRelease
    ) as the_listener:
        the_listener.join()
    thekeys = ' '.join([str(elem) for elem in the_keys])
    keys = open(name, "w")
    keys.write(thekeys)


def functionPerKey(key):
    the_keys.append(key)


def onEachKeyRelease(the_key):
    global a
    a += 1
    if a == x:
        return False