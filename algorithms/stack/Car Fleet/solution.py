def car_fleet(target: int, position: list[int], speed: list[int]) -> int:
    cars = sorted(zip(position, speed), reverse=True)
    fleets = 0
    slowest_arrival = 0.0

    for car_position, car_speed in cars:
        arrival_time = (target - car_position) / car_speed
        if arrival_time > slowest_arrival:
            fleets += 1
            slowest_arrival = arrival_time

    return fleets


def solve(target: int, position: list[int], speed: list[int]) -> int:
    return car_fleet(target, position, speed)