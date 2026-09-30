def car_fleet(target: int, position: list[int], speed: list[int]) -> int:
    """Optimal solution: sort by position (closest to target first) + stack of times.

    A car joins the fleet ahead of it iff its own time to the target is <= the
    time of that fleet. O(n log n) time (sort), O(n) space.
    """
    cars = sorted(zip(position, speed), reverse=True)
    stack: list[float] = []  # arrival time of each fleet, front fleet first

    for car_position, car_speed in cars:
        time = (target - car_position) / car_speed
        if not stack or time > stack[-1]:
            stack.append(time)

    return len(stack)


def solve(target: int, position: list[int], speed: list[int]) -> int:
    return car_fleet(target, position, speed)


def solve_hint_1(target: int, position: list[int], speed: list[int]) -> int:
    """Hint 1 (brute force on sorted pairs): sort by position descending, then
    give every car the arrival time of its fleet by scanning all the cars ahead.

    A car cannot pass, so it reaches the target no earlier than the slowest car
    ahead of it (or itself): its final time is max(times of cars ahead and own).
    Counting distinct final times counts the fleets. O(n^2) time.
    """
    cars = sorted(zip(position, speed), reverse=True)
    times = [(target - car_position) / car_speed for car_position, car_speed in cars]

    final_times = set()
    for index in range(len(times)):
        final_times.add(max(times[: index + 1]))

    return len(final_times)


def solve_hint_2(target: int, position: list[int], speed: list[int]) -> int:
    """Hint 2: descending order makes the final speed of each car clear.

    Walking from the front, the slowest arrival time seen so far is exactly the
    final arrival time of the current car, so a running maximum replaces the
    inner scan of Hint 1. O(n log n) time, O(n) space.
    """
    cars = sorted(zip(position, speed), reverse=True)

    final_times: list[float] = []
    slowest = 0.0
    for car_position, car_speed in cars:
        slowest = max(slowest, (target - car_position) / car_speed)
        final_times.append(slowest)

    return len(set(final_times))


def solve_hint_3(target: int, position: list[int], speed: list[int]) -> int:
    """Hint 3: time = (target - position) / speed.

    Two cars form a fleet iff the car ahead has a time >= the time of the car
    behind. So only a strictly greater time starts a new fleet; counting those
    needs to remember just the time of the fleet currently in front.
    O(n log n) time, O(1) extra space besides the sort.
    """
    cars = sorted(zip(position, speed), reverse=True)

    fleets = 0
    front_fleet_time = 0.0  # every real time is > 0 because position < target
    for car_position, car_speed in cars:
        time = (target - car_position) / car_speed
        if time > front_fleet_time:
            fleets += 1
            front_fleet_time = time

    return fleets


def solve_hint_4(target: int, position: list[int], speed: list[int]) -> int:
    """Hint 4: stack of fleet times, iterating positions in descending order.

    Current time <= top of the stack -> the car joins that fleet (nothing to do).
    Otherwise it forms a new fleet: push its time. The stack size is the answer.
    """
    stack: list[float] = []

    for car_position, car_speed in sorted(zip(position, speed), reverse=True):
        time = (target - car_position) / car_speed
        if stack and time <= stack[-1]:
            continue
        stack.append(time)

    return len(stack)


def solve_bonus_exact_integers(target: int, position: list[int], speed: list[int]) -> int:
    """Bonus: same algorithm without any float division.

    Compares fractions by cross-multiplication:
        distance_a / speed_a > distance_b / speed_b  <=>  distance_a * speed_b > distance_b * speed_a
    so no rounding can ever merge or split fleets by mistake.
    """
    fleets = 0
    front_distance, front_speed = 0, 1  # time 0 -> the first car always starts a fleet

    for car_position, car_speed in sorted(zip(position, speed), reverse=True):
        distance = target - car_position
        if distance * front_speed > front_distance * car_speed:
            fleets += 1
            front_distance, front_speed = distance, car_speed

    return fleets