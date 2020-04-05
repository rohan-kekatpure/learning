import numpy as np
import matplotlib.pyplot as pl
from scipy.integrate import simps


def generate_points(n_points):
    theta = np.linspace(-np.pi, np.pi, n_points)
    radius = np.random.uniform(0.5, 1.5, size=(n_points,))
    return radius, theta

def pol2cart(r, theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    x = np.hstack((x, x[0]))
    y = np.hstack((y, y[0]))
    return x, y

def perimeter(r, theta):
    x, y = pol2cart(r, theta)
    dx = np.diff(x)
    dy = np.diff(y)
    perim = np.sqrt((dx*dx + dy * dy)).sum()
    return perim


def area(r, theta):
    return simps(r * r, theta) / 2.0

def hill_climbing(r, theta, n_iterations=1000, save_images=False):
    n_points = r.shape[0]
    constr_val = 2 * np.pi
    best_r = r.copy()
    best_area = area(best_r, theta)
    x0, y0 = pol2cart(r, theta)
    for i in range(n_iterations):
        if i % 1000 == 0:
            print('iteration -> {}'.format(i))
        old_r = r.copy()
        j = np.random.randint(0, n_points)
        r[j] += np.random.uniform(-.01, .01)
        new_perim = perimeter(r, theta)
        r *= constr_val / new_perim
        new_area = area(r, theta)
        if save_images and (i % 10 == 0):
            x1, y1 = pol2cart(r, theta)
            pl.close('all')
            _, ax = pl.subplots()
            ax.plot(x0, y0, 'r-', lw=1)
            ax.plot(x1, y1, 'g-', lw=1)
            ax.set_xlim([-1.2, 1.2])
            ax.set_ylim([-1.2, 1.2])
            ax.set_aspect('equal', 'box')
            pl.savefig('./img_hill_climbing/image_{}.png'.format(i))

        if new_area > best_area:
            best_area = new_area
            best_r = r
        else:
            r = old_r

    return best_r, theta

def gradient_descent(r, theta, learning_rate, reg_param, n_iterations=1000, save_images=False):
    alpha = learning_rate
    constr_val = 2 * np.pi
    x0, y0 = pol2cart(r, theta)
    delta_theta = theta[1] - theta[0]
    for i in range(n_iterations):
        if i % 10 == 0:
            print('iteration -> {}'.format(i))

        r += 0.5 * alpha * delta_theta * r + reg_param
        new_perim = perimeter(r, theta)
        r *= constr_val / new_perim

        if save_images and (i % 5 == 0):
            x1, y1 = pol2cart(r, theta)
            pl.close('all')
            _, ax = pl.subplots()
            ax.plot(x0, y0, 'r-', lw=1)
            ax.plot(x1, y1, 'g-', lw=1)
            ax.set_xlim([-1.2, 1.2])
            ax.set_ylim([-1.2, 1.2])
            ax.set_aspect('equal', 'box')
            pl.savefig('./img_gradient_descent/image_{}.png'.format(i))

    return r, theta


def main():
    r_, theta_ = generate_points(64)
    P, A = perimeter(r_, theta_), area(r_, theta_)
    r_ *= (2 * np.pi) / P
    print(perimeter(r_, theta_), area(r_, theta_))

    best_r, best_theta = hill_climbing(r_.copy(), theta_.copy(), n_iterations=25000, save_images=True)
    print(perimeter(best_r, best_theta), area(best_r, best_theta))

    best_r, best_theta = gradient_descent(r_.copy(), theta_.copy(), 0.01, 0.01, n_iterations=500, save_images=True)
    print(perimeter(best_r, best_theta), area(best_r, best_theta))


if __name__ == '__main__':
    main()
