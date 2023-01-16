"""run_2_class_2_feature_iris_data.py
YOU SHOULD NOT NEED TO EDIT THIS FILE OR TURN IT IN.
HOWEVER, YOU ARE WELCOME TO EDIT THE FILE TO EXPLORE
POSSIBLE ADJUSTMENTS TO PARAMETERS.

Train a perceptron on the first 10 examples of iris setosa
and the first 10 examples of iris versicolor, considering
only sepal length and petal length as features.

Then test with the remaining 40 examples of each.
Extends the Class PlotBinaryPerceptron

Version 1.1, Prashant Rangarajan and S. Tanimoto, May 11, 2021. Univ. of Washington.
"""

from binary_perceptron import BinaryPerceptron # Your implementation of binary perceptron
from plot_bp import PlotBinaryPerceptron
import csv  # For loading data.
from matplotlib import pyplot as plt  # For creating plots. 


class PlotMultiBPOneVsAll(PlotBinaryPerceptron):
    """
    Plots the Binary Perceptron after training it on the Iris dataset
    ---
    Extends the class PlotBinaryPerceptron
    """

    def __init__(self, bp, plot_all=True, n_epochs=50):
        super().__init__(bp, plot_all, n_epochs) # Calls the constructor of the super class
        # you can choose "one" of "one-vs-all" by selecting a variable below
        self.POSITIVE=0
        #self.POSITIVE=1
        #self.POSITIVE=2
        #PROT_ALL become false because we have to indicate only final plot separator
        self.PLOT_ALL=False

    def read_data(self):
        """
        Read data from the Iris dataset with 2 features and 2 classes
        for both training and testing.
        ---
        Overrides the method in PlotBinaryPerceptron
        """
        data_as_strings = list(csv.reader(open('synthetic_data.csv'), delimiter=','))
        self.TRAINING_DATA = [[float(f1), float(f2), int(c)]
                              for [f1, f2, c] in data_as_strings]


    def plot_separator(self, w0, w1, w2):
        """
        Add to the plot so far a line that best represents
        the current set of weights, where we are interpreting
        them as w0*x + w1*y + w2 = 0.
        x
        """
        y1 = (-w2 - w0 * self.X_MIN) / w1
        y2 = (-w2 - w0 * self.X_MAX) / w1
        if self.PLOT_ALL:
            plt.plot([self.X_MIN, self.X_MAX], [y1, y2], label='Epoch {i}'.format(i=self.PLOTLINE_COUNT))
        else:
            plt.plot([self.X_MIN, self.X_MAX], [y1, y2], label='Final Separator')
        self.PLOTLINE_COUNT += 1

    def train(self, verbose=False):
        """
        Trains the Binary perceptron
        verbose: If True, prints out the weights and changed count
                at every epoch
        """
        self.read_data()
        
        for j in range(len(self.TRAINING_DATA)):
            if self.TRAINING_DATA[j][-1] == self.POSITIVE:
                self.TRAINING_DATA[j][-1] = +1
            else:
                self.TRAINING_DATA[j][-1] = -1

        self.plot_2d_points(self.TRAINING_DATA)
        
        for i in range(self.MAX_EPOCHS):
            changed_count = self.bp.train_for_an_epoch(self.TRAINING_DATA)
            if changed_count == 0:
                print("Converged in ", i, " epochs.")
                print("TRAINING IS DONE")
                if not self.PLOT_ALL:
                    self.plot_separator(*self.bp.weights)
                return
            if verbose:
                print(f"changed_count= {changed_count}")
                print(f"Weights:\n{self.bp.weights}")
            if self.PLOT_ALL:
                self.plot_separator(*self.bp.weights)
        self.plot_separator(*self.bp.weights)
        print(f"Training did not converge in {self.MAX_EPOCHS} epochs.")

    def plot(self):
        """
        Plots the dataset as well as the binary classifier
        ---
        Overrides the method in PlotBinaryPreceptron
        """
        plt.title("Plot with class 0 as the positive class")
        plt.xlabel("Sepal length")
        plt.ylabel("Petal length")
        plt.legend(loc='best')
        plt.show()



if __name__=='__main__':
    binary_perceptron = BinaryPerceptron(alpha=0.5)
    pbp = PlotMultiBPOneVsAll(binary_perceptron)
    pbp.train()
    pbp.test()
    pbp.plot()