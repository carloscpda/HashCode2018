import numpy as np

a = 0   # The row of the start intersection
b = 1   # The column of the start intersection
x = 2   # The row of the finish intersection
y = 3   # The column of the finish intersection
s = 4   # The earliest start
f = 5   # The latest finish
c = 2   # Contador

output_file = "../data/output.out"

def main():
    # PARSER
    header = np.loadtxt("../data/a_example_header.in", dtype=int)
    data = np.loadtxt("../data/a_example.in", dtype=int)

    n_rows = header[0]
    n_cols = header[1]
    n_cars = header[2]
    n_rides = header[3]
    bonus = header[4]
    t_steps = header[5]

    cars = [[0 for z in range(3)] for z2 in range(n_cars)]
    max_distance = ride_distance(0, 0, n_rows, n_cols)

    output = [[0] for z2 in range(n_cars)]

    a_step = 0

    for a_step in range(0, t_steps):
        print('Actual step is', a_step)

        for idx_car, car in enumerate(cars):
            chosen_ride = -1
            if car[c] is not 0:
                car[c] = car[c] - 1


            # Elegimos coche vacio
            if car[c] == 0:
                for idx_ride, ride in enumerate(data):
                    travel_distance = ride_distance(ride[a], ride[b], ride[x], ride[y])
                    car_to_ride_distance = max_distance

                    if ride_distance(car[a], car[b], ride[a], ride[b]) <= car_to_ride_distance:
                        car_to_ride_distance = min(car_to_ride_distance, ride_distance(car[a], car[b], ride[a], ride[b]))
                        total_distance = travel_distance + car_to_ride_distance

                        if total_distance <= ride[f] - a_step and total_distance <= ride[f] - ride[s]:
                            chosen_ride = idx_ride


                if chosen_ride != -1:
                    car[c] = total_distance
                    if data[chosen_ride][s] - a_step - car_to_ride_distance > 0:
                        car[c] += data[chosen_ride][s] - a_step - car_to_ride_distance
                    car[a] = data[chosen_ride][x]
                    car[b] = data[chosen_ride][y]
                    data[chosen_ride][f] = 0
                    #print("Ride:", chosen_ride, "Car:", idx_car)
                    output[idx_car].append(chosen_ride)
                    output[idx_car][0] += 1

    for out in output:
        for idx, char in enumerate(out):
            with open(output_file, "a") as my_file:
                if idx == 0:
                    my_file.write(str(char))
                else:
                    my_file.write(" " + str(char))

        with open(output_file, "a") as my_file:
            my_file.write("\n")


def ride_distance(a, b, x, y):
    return abs(y-b)+abs(x-a)

if __name__ == "__main__":
    main()
