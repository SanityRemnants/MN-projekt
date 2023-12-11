import csv
import numpy as np
from matplotlib import pyplot
def interpolation_function(points):
    #n intervals
    n = len(points) - 1

    A = np.zeros([4*n,4*n])
    b = np.zeros([4*n,1])
    #Sj(xj) = f(xj)
    for i in range(n):
        x,y = points[i]
        A[4*i+3][4*i+3] = float(1)
        b[4*i+3] = float(y)
        #ai = f(xi)

    # Sj(xj+1) = f(xj+1)
    for i in range(n):
        x1, y1 = points[i + 1]
        x0, y0 = points[i]
        h = float(x1) - float(x0)
        A[4 * i + 2][4 * i] = h ** 3
        A[4 * i + 2][4 * i + 1] = h ** 2
        A[4 * i + 2][4 * i + 2] = h
        A[4 * i + 2][4 * i + 3] = 1
        b[4 * i + 2] = float(y1)
        #aj + bjh + cjh^2 + djh^3 = f (xj+1)

    #inner points
    for i in range(n - 1):
        x1, y1 = points[i + 1]
        x0, y0 = points[i]
        h = float(x1) - float(x0)
        A[4 * i][4 * i] = 3 * (h ** 2)
        A[4 * i][4 * i + 1] = 2 * h
        A[4 * i][4 * i + 2] = 1
        A[4 * i][4 * (i + 1) + 2] = -1
        b[4 * i] = float(0)
    for i in range(n - 1):
        x1, y1 = points[i + 1]
        x0, y0 = points[i]
        h = float(x1) - float(x0)
        A[4 * (i + 1) + 1][4 * i] = 6 * h
        A[4 * (i + 1) + 1][4 * i + 1] = 2
        A[4 * (i + 1) + 1][4 * (i + 1) + 1] = -2
        b[4 * (i + 1) + 1] = float(0)
    #first point
    A[1][1] = 2
    b[1] = float(0)
    # last point
    x1, y1 = points[-1]
    x0, y0 = points[-2]
    h = float(x1) - float(x0)
    A[-4][1] = 2
    A[-4][-4] = 6 * h
    b[-4] = float(0)

    par = np.linalg.solve(A,b)

    def f(x):
        param_array = []
        row = []
        #create parameter matrix for intervals
        for parameter in par:
            row.append(parameter)
            if len(row) == 4:
                param_array.append(row.copy())
                row.clear()
        #find correct interval
        for i in range(1, n+1):
            xi, yi = points[i - 1]
            xj, yj = points[i]
            if float(xi) <= x <= float(xj):
                a, b, c, d = param_array[i - 1]
                h = x - float(xi)
                return a * (h ** 3) + b * (h ** 2) + c * h + d
        #if outside of any intervals return edge value
        x0,y0 = points[0]
        xn,yn = points[len(points)-1]
        if x < float(x0):
            return y0
        else:
            return yn
    return f

def interpolate_spline(step):
    f = open('./2018_paths/GlebiaChallengera.csv', 'r')
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
    pyplot.title('Przybliżenie interpolacją Splajnami 3. stopnia, ' + str(len(interpolation_points)) + ' punkty(ów)')
    pyplot.suptitle("Glebia Challengera")
    pyplot.grid()
    pyplot.show()
