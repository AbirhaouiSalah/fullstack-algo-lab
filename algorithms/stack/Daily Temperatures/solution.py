def daily_temperatures(temperatures: list[int]) -> list[int]:
    waits = [0] * len(temperatures)
    warmer_days: list[int] = []

    for day, temperature in enumerate(temperatures):
        while warmer_days and temperature > temperatures[warmer_days[-1]]:
            previous_day = warmer_days.pop()
            waits[previous_day] = day - previous_day
        warmer_days.append(day)

    return waits


def solve(temperatures: list[int]) -> list[int]:
    return daily_temperatures(temperatures)