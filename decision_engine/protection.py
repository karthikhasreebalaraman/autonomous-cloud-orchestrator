import time

MIN_CONTAINERS = 2
MAX_CONTAINERS = 6
COOLDOWN_SECONDS = 60

_last_action_time = 0


def can_scale_up(running_containers):
    global _last_action_time

    if running_containers >= MAX_CONTAINERS:
        return False, "Maximum container limit reached"

    if time.time() - _last_action_time < COOLDOWN_SECONDS:
        remaining = int(
            COOLDOWN_SECONDS - (time.time() - _last_action_time)
        )
        return False, f"Cooldown active: wait {remaining} seconds"

    return True, "Scale up allowed"


def can_scale_down(running_containers):
    global _last_action_time

    if running_containers <= MIN_CONTAINERS:
        return False, "Minimum container limit reached"

    if time.time() - _last_action_time < COOLDOWN_SECONDS:
        remaining = int(
            COOLDOWN_SECONDS - (time.time() - _last_action_time)
        )
        return False, f"Cooldown active: wait {remaining} seconds"

    return True, "Scale down allowed"


def record_action():
    global _last_action_time
    _last_action_time = time.time()


if __name__ == "__main__":

    print("========================================")
    print("DECISION ENGINE PROTECTION")
    print("========================================")

    print(f"Minimum containers : {MIN_CONTAINERS}")
    print(f"Maximum containers : {MAX_CONTAINERS}")
    print(f"Cooldown           : {COOLDOWN_SECONDS} seconds")

    allowed, message = can_scale_up(3)

    print(f"Scale up allowed   : {allowed}")
    print(f"Message            : {message}")

    record_action()

    allowed, message = can_scale_up(3)

    print(f"After action       : {allowed}")
    print(f"Message            : {message}")

    print("========================================")