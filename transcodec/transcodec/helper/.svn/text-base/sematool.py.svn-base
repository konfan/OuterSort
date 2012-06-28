import threading

def semaphore_init(maxValue, initValue):
    """
    create a semaphore with max value = maxValue
    and init value = initValue
    """
    assert maxValue >= initValue
    sema = threading.BoundedSemaphore(value = maxValue)
    for i in range(maxValue - initValue):
        sema.acquire()
    return sema

def sema_wait(sema, block = 1):
    return sema.acquire(block)

def sema_signal(sema):
    sema.release()
