import numpy as np
import math

# constants
a = 0  # The row of the start intersection
b = 1  # The column of the start intersection
x = 2  # The row of the finish intersection
y = 3  # The column of the finish intersection
s = 4  # The earliest start
f = 5  # The latest finish
c = 2  # Steps to be available
ride_done = -1

# global variables
data = n_rows = n_cols = n_cars = n_rides = bonus = t_steps = 0


def parser_input(exercise):
    input_file = "../data/" + exercise + ".in"
    with open(input_file, 'r') as input_file_str:
        header_str = input_file_str.readline().replace('\n', '')

    input_file_str.close()

    header = np.fromstring(header_str, sep=' ', dtype=int)

    global data, n_rows, n_cols, n_cars, n_rides, bonus, t_steps
    data = np.loadtxt(input_file, dtype=int, skiprows=1)
    n_rows = header[0]
    n_cols = header[1]
    n_cars = header[2]
    n_rides = header[3]
    bonus = header[4]
    t_steps = header[5]


def save_output(exercise, output):
    output_file_path = "../data/" + exercise + ".out"
    output_file = open(output_file_path, 'w')
    output_file.truncate()
    for out in output:
        for idx, char in enumerate(out):
            if idx == 0:
                output_file.write(str(char))
            else:
                output_file.write(" " + str(char))

        output_file.write("\n")
    output_file.close()


def ride_distance(a, b, x, y):
    return abs(y - b) + abs(x - a)


# TODO Si llega justo a tiempo no da puntos a no ser que si de el bonus ¿?¿?
def loop(exercise):
    parser_input(exercise)
    cars = [[0 for _ in range(3)] for _ in range(n_cars)]
    output = [[0] for _ in range(n_cars)]

    for a_step in range(0, t_steps):
        print(a_step)

        for idx_car, car in enumerate(cars):
            chosen_ride = -1
            if car[c] is not 0:
                car[c] = car[c] - 1

            # Elegimos coche vacio
            if car[c] == 0:
                points = 0
                steps = t_steps
                for idx_ride, ride in enumerate(data):
                    if ride[s] == -1:
                        continue
                    travel_distance = ride_distance(ride[a], ride[b], ride[x], ride[y])
                    a_points = travel_distance
                    car_to_ride_distance = ride_distance(car[a], car[b], ride[a], ride[b])
                    total_distance = travel_distance + car_to_ride_distance

                    if total_distance <= ride[f] - a_step and total_distance <= ride[f] - ride[s]:
                        wait_time = ride[s] - a_step

                        if wait_time - car_to_ride_distance > 0:
                            total_distance += wait_time - car_to_ride_distance

                        a_points -= wait_time
                        if car_to_ride_distance + a_step == ride[s]:
                            a_points += bonus

                        if a_points >= points:
                            chosen_ride = idx_ride
                            points = a_points
                            steps = total_distance

                if chosen_ride != -1:
                    car[c] = steps
                    car[a] = data[chosen_ride][x]
                    car[b] = data[chosen_ride][y]
                    data[chosen_ride][s] = ride_done
                    data[chosen_ride][f] = 0
                    output[idx_car].append(chosen_ride)
                    output[idx_car][0] += 1

    print("\n")
    save_output(exercise, output)


def main():
    for exercise in ["a_example", "b_should_be_easy", "c_no_hurry", "d_metropolis", "e_high_bonus"]:
        print("Start exercise ", exercise)
        loop(exercise)
        print("Finish exercise ", exercise)


if __name__ == "__main__":
    main()
