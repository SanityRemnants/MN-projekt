import csv
from matplotlib import pyplot

def interpolation_function(points):
    def f(x):
        result = 0
        n = len(points)
        for i in range(n):
            xi, yi = points[i]
            base = 1
            for j in range(n):
                if i == j:
                    continue
                else:
                    xj, yj = points[j]
                    base *= (float(x) - float(xj))/float(float(xi) - float(xj))
            result += float(yi) * base
        return result
    return f
def interpolate_lagrange(step):
    f = open('./2018_paths/WielkiKanionKolorado.csv', 'r')
    data = list(csv.reader(f))

    interpolation_points = data[0::step]
    interpolation_points.append(data[len(data)-1])
    func = interpolation_function(interpolation_points)

    #data for the plot
    distance = []
    height = []
    interpolated_height = []
    for point in data:
        x, y = point
        distance.append(float(x))
        height.append(float(y))
        #interpolated points
        interpolated_height.append(func(float(x)))
    #points used for interpolation
    train_distance = []
    train_height = []
    for point in interpolation_points:
        x, y = point
        train_distance.append(float(x))
        train_height.append(func(float(x)))
    #plot
    pyplot.plot(distance, height, 'r.', label='pełne dane')
    pyplot.plot(distance, interpolated_height, color='blue', label='funkcja interpolująca')
    pyplot.plot(train_distance, train_height, 'g.', label='dane do interpolacji')
    pyplot.legend()
    pyplot.ylabel('Wysokość')
    pyplot.xlabel('Odległość')
    pyplot.title('Przybliżenie interpolacją Lagrange\'a, ' + str(len(interpolation_points)) + ' punkty(ów)')
    pyplot.suptitle("Wielki Kanion Kolorado")
    pyplot.grid()
    pyplot.show()
