import math
import numpy as np

import matplotlib.pyplot as plt
from sklearn_lvq.utils import _tango_color

from glvq.plot_2d import to_tango_colors
from glvq.plot_2d import plot2d

from sklearn.utils import shuffle
from sklearn_lvq.glvq import GlvqModel
from quad_fair_glvq import MeanDiffGlvqModel as FairGlvqModel
from normalized_fair_glvq import NormMeanDiffGlvqModel as NormFairGlvqModel


# TODO: WORK IN PROGRESS
class DataGen:

    def __init__(self, verbose=False):
        """
            Constructor. More needed?

            Parameters
            ----------
            verbose: bool
                Flag to show status prints.

        """
        # number of data points     - Likely
        # proportion of subclasses  - Likely
        # number of features        - Maybe later?
        # number of subclasses      - necessary???
        self.verbose = verbose

        self.color_0 = 'skyblue'
        self.color_1 = 'scarletred'
        self.color_pos = 'chocolate'
        
        pass

    # TODO: Add parameter to shift bubbles relative to each other
    def generate_two_bubbles(self, number_data_points, proportion_0, proportion_0_urban, proportion_1_urban,
                             proportion_0_pay, proportion_1_pay, std_feature_1=0.2, std_feature_2=0.2):
        """
            Generates data set around two bubbles (normal distributions).

            Parameters
            ----------
            number_data_points: int
                Size of the data set.

            proportion_0: float in interval [0, 1]
                Proportion of the protected subclass.

            proportion_0_urban: float in interval [0, 1]
                Proportion of the protected subclass in urban neighbourhoods.

            proportion_1_urban: float in interval [0, 1]
                Proportion of the un-protected subclass in urban neighbourhoods.

            proportion_0_pay: float in interval [0, 1]
                Proportion of the protected subclass that repays their credit.

            proportion_1_pay: float in interval [0, 1]
                Proportion of the un-protected subclass that repays their credit.

            std_feature_1: float in interval [0, 1]
                Standard deviation of first feature in normal distributions to create bubbles.

            std_feature_2: float in interval [0, 1]
                Standard deviation of second feature in normal distributions to create bubbles.

            Returns
            -------
            r : float
                measure of discrimination
            X_full:
            C_full:
            Y_full:

        """

        # proportion of non-white people who do not pay their money back
        proportion_0_dont_pay = 1 - proportion_0_pay
        # proportion of white people who do not pay their money back
        proportion_1_dont_pay = 1 - proportion_1_pay

        # proportion of non-white people in suburban neighbourhoods
        proportion_0_suburban = 1 - proportion_0_urban

        # number of people living in urban neighbourhoods
        m_urban = int(number_data_points * (1 - proportion_0) * proportion_1_urban +
                      number_data_points * proportion_0 * proportion_0_urban)
        # number of people living in suburban neighbourhoods
        m_suburb = number_data_points - m_urban
        if self.verbose:
            print("----")
            print("Total number of people in urban neighbourhoods: \t{}".format(m_urban))
            print("Total number of people in suburban neighbourhoods: \t{}".format(m_suburb))
            print("----")

        X_urban = np.random.randn(m_urban, 2).dot(np.array([[std_feature_1, 0], [0, std_feature_2]]))
        X_suburb = np.random.randn(m_suburb, 2).dot(np.array([[std_feature_1, 0], [0, std_feature_2]]))

        # shift suburban population
        X_suburb += np.array([1, 0])

        # sort data points in both sets
        X_urban_sorted = sorted(X_urban, key=lambda x: x[1], reverse=False)

        # generate a vector C denoting the racial information
        C = [np.zeros(m_urban, dtype=bool)]

        # number of all non-whites living in urban neighbourhoods
        m0 = int(proportion_0_urban * proportion_0 * number_data_points)
        C[0][m0:] = True

        if self.verbose:
            print("Number of \tnon-white \turban: \t\t{}".format(m0))
            print("Number of \twhite \t\turban: \t\t{}".format(m_urban - m0))

        X_suburb_sorted = sorted(X_suburb, key=lambda x: x[1], reverse=False)
        C.append(np.zeros(m_suburb, dtype=bool))
        # number of all non-whites living in suburban neighbourhoods
        m1 = int(proportion_0_suburban * proportion_0 * number_data_points)
        C[1][m1:] = True

        if self.verbose:
            print("Number of \tnon-white \tsuburban: \t{}".format(m1))
            print("Number of \twhite \t\tsuburban: \t{}".format(m_suburb - m1))
            print("----")

        # generate a vector Y for urban area denoting the actual information about whether
        # money was paid back or not
        Y = [np.zeros(m_urban, dtype=bool)]
        # set
        m00 = int(m0 * proportion_0_dont_pay)
        Y[0][m00:m0] = True
        Y[0][:m0] = shuffle(Y[0][:m0])

        m10 = int((m_urban - m0) * proportion_1_dont_pay)
        Y[0][m0 + m10:] = True
        Y[0][m0:] = shuffle(Y[0][m0:])

        if self.verbose:
            print("Number of \turban \t\tnon-white \tdo not pay\t(m00): {}".format(m00))
            print("Number of \turban \t\twhite \t\tdo not pay\t(m10): {}".format(m10))

        # generate a vector Y for suburban area denoting the actual information about whether
        # money was paid back or not
        Y.append(np.zeros(m_suburb, dtype=bool))
        m00 = int(m1 * proportion_0_dont_pay)
        Y[1][m00:m0] = True
        Y[1][:m0] = shuffle(Y[1][:m0])

        m10 = int((m_suburb - m1) * proportion_1_dont_pay)
        Y[1][m0 + m10:] = True
        Y[1][m0:] = shuffle(Y[1][m0:])

        if self.verbose:
            print("Number of \tsuburban \tnon-white \tdo not pay\t(m00): {}".format(m00))
            print("Number of \tsuburban \twhite \t\tdo not pay\t(m10): {}".format(m10))
            print("----")

        X_full = np.concatenate((X_urban_sorted, X_suburb_sorted))
        C_full = np.concatenate((C[0], C[1]))
        Y_full = np.concatenate((Y[0], Y[1]))

        return X_full, C_full, Y_full

    # TODO: handle Y_pred = None
    # TODO: Add some way to use the model to plot prototypes
    def prepare_plot(self, X, C, Y, Y_pred = None, prototypes=None):
        """
            Generated plot information for a given data set with given classification.

            Parameters
            ----------
            X: np.ndarray of floats
                Array containing all data point coordinates.

            C: np.array of bool
                Array containing all data point subclass memberships.

            Y: np.array of bool
                Array containing all data point outcomes.

            Y_pred: np.array of bool
                Array containing all data point predicted outcomes.

            prototypes: np.ndarray of floats
                Array of prototype locations.

            Returns
            -------
            ax: subplot info
                Contains prepared plot details.
        """
        # non-white: do not pay
        log00 = np.logical_and(np.logical_not(C), np.logical_not(Y))
        # non-white: pay
        log01 = np.logical_and(np.logical_not(C), Y)

        # white: do not pay
        log10 = np.logical_and(C, np.logical_not(Y))
        # white: pay
        log11 = np.logical_and(C, Y)

        # Plot the data and the prototypes as well
        fig = plt.figure()
        fig.canvas.set_window_title("LVQ with continuous distance to city center")
        ax = fig.add_subplot(111)
        ax.set_xlabel("Distance from City Center")
        ax.set_ylabel("Income")

        if Y_pred is None:
            # non-white: do not pay
            ax.scatter(X[log00, 0], X[log00, 1], c=_tango_color(self.color_0, 0),
                       edgecolors=_tango_color(self.color_0, 2), marker='o')
            # non-white: pay
            ax.scatter(X[log01, 0], X[log01, 1], c=_tango_color(self.color_0, 0),
                       edgecolors=_tango_color(self.color_0, 2), marker='s')
            # white: do not pay
            ax.scatter(X[log10, 0], X[log10, 1], c=_tango_color(self.color_1, 0),
                       edgecolors=_tango_color(self.color_1, 2), marker='o')
            # white: pay
            ax.scatter(X[log11, 0], X[log11, 1], c=_tango_color(self.color_1, 0),
                       edgecolors=_tango_color(self.color_1, 2), marker='s')
        else:        
            if self.verbose:
                n_pos = list(Y_pred).count(True)
                print("Number of positive values in Y_pred: {}".format(n_pos))
    
            # Gather indices based on classification
    
            # non-white | do not pay | classified positive
            log00_pos = np.logical_and(log00, Y_pred)
            # non-white | pay | classified positive
            log01_pos = np.logical_and(log01, Y_pred)
            # white | do not pay | classified positive
            log10_pos = np.logical_and(log10, Y_pred)
            # white | pay | classified positive
            log11_pos = np.logical_and(log11, Y_pred)

            if self.verbose:
                n_pos = list(log00_pos).count(True)
                print("Number of positive values in log01_pos: {} of {}".format(n_pos, len(log01_pos)))
    
            # non-white | do not pay | classified negative
            log00_neg = np.logical_and(log00, np.logical_not(Y_pred))
            # non-white | pay | classified negative
            log01_neg = np.logical_and(log01, np.logical_not(Y_pred))
    
            # white| do not pay | classified negative
            log10_neg = np.logical_and(log10, np.logical_not(Y_pred))
            # white | pay  | classified negative
            log11_neg = np.logical_and(log11, np.logical_not(Y_pred))
    
            if self.verbose:
                sum_log = list(log00_pos).count(True) + list(log01_pos).count(True) \
                          + list(log10_pos).count(True) + list(log11_pos).count(True) \
                          + list(log00_neg).count(True) + list(log01_neg).count(True) \
                          + list(log10_neg).count(True) + list(log11_neg).count(True)
                print("Sum over all logs is: {}".format(sum_log))
    
            # non-white: do not pay
            ax.scatter(X[log00_neg, 0], X[log00_neg, 1], c=_tango_color(self.color_0, 0),
                       edgecolors=_tango_color(self.color_0, 2), marker='o')
            # non-white: pay
            ax.scatter(X[log01_neg, 0], X[log01_neg, 1], c=_tango_color(self.color_0, 0),
                       edgecolors=_tango_color(self.color_0, 2), marker='s')
            # white: do not pay
            ax.scatter(X[log10_neg, 0], X[log10_neg, 1], c=_tango_color(self.color_1, 0),
                       edgecolors=_tango_color(self.color_1, 2), marker='o')
            # white: pay
            ax.scatter(X[log11_neg, 0], X[log11_neg, 1], c=_tango_color(self.color_1, 0),
                       edgecolors=_tango_color(self.color_1, 2), marker='s')
    
            # non-white: do not pay
            ax.scatter(X[log00_pos, 0], X[log00_pos, 1], c=_tango_color(self.color_pos, 0),
                       edgecolors=_tango_color(self.color_0, 2), marker='o')
            # non-white: pay
            ax.scatter(X[log01_pos, 0], X[log01_pos, 1], c=_tango_color(self.color_pos, 0),
                       edgecolors=_tango_color(self.color_0, 2), marker='s')
            # white: do not pay
            ax.scatter(X[log10_pos, 0], X[log10_pos, 1], c=_tango_color(self.color_pos, 0),
                       edgecolors=_tango_color(self.color_1, 2), marker='o')
            # white: pay
            ax.scatter(X[log11_pos, 0], X[log11_pos, 1], c=_tango_color(self.color_pos, 0),
                       edgecolors=_tango_color(self.color_1, 2), marker='s')
            if prototypes is not None:
                ax.scatter(prototypes[0, 0], prototypes[0, 1], c=_tango_color(self.color_0, 1),
                           edgecolors=_tango_color(self.color_0, 2), linewidths=2, s=150, marker='D')
                ax.scatter(prototypes[1, 0], prototypes[1, 1], c=_tango_color(self.color_1, 1),
                           edgecolors=_tango_color(self.color_1, 2), linewidths=2, s=150, marker='D')
        return ax

    def plot_prepared_dist(self, ax):
        """
            Plots a prepared data set.

            Parameters
            ----------
            ax: axes
                Axes object that holds the plotting information.
        """
        ax.plot()
        plt.show()
        return

    def plot_dist(self, X, C, Y, Y_pred, prototypes=None):
        """
            Prints classification of a given data set.

            Parameters
            ----------
            X: np.ndarray of floats
                Array containing all data point coordinates.

            C: np.array of bool
                Array containing all data point subclass memberships.

            Y: np.array of bool
                Array containing all data point outcomes.

            Y_pred: np.array of bool
                Array containing all data point predicted outcomes.

            prototypes: np.ndarray of floats
                Array of prototype locations.

        """
        ax = self.prepare_plot(X, C, Y, Y_pred, prototypes)
        self.plot_prepared_dist(ax)
        return

    def print_dist_glvq(self, X, C, Y):
        """
            Prints classification of a given data set with GLVQ.

            Parameters
            ----------
            X: np.ndarray of floats
                Array containing all data point coordinates.

            C: np.array of bool
                Array containing all data point subclass memberships.

            Y: np.array of bool
                Array containing all data point outcomes.
        """

        # Train a GLVQ model
        model = GlvqModel()
        model.fit(X, Y)

        # find prediction of model for all points
        Y_pred = model.predict(X)

        if self.verbose:
            n_pos = list(Y_pred).count(True)
            print("Number of positive values in Y_pred: {}".format(n_pos))
            
        self.plot_dist(X, C, Y, Y_pred, model.w_)
        return
