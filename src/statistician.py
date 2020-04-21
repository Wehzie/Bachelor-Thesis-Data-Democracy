

class Statistician(object):

    def __init__(self, sim: object):
        self.sim = sim
        self.money = {"f": [], "hh": []}

    ######## ######## ######## METHODS ######## ######## ########

    def sum_f_money(self) -> float:
        f_sum = 0
        for f in self.sim.firm_list:
            f_sum += f.money
        return f_sum
    
    def sum_hh_money(self) -> float:
        hh_sum = 0
        for hh in self.sim.hh_list:
            hh_sum += hh.money
        return hh_sum
    
    def up_stat(self):
        self.money["f"].append(self.sum_f_money())
        self.money["hh"].append(self.sum_hh_money())

    # TODO: think about days within a month
    # plot hh and firm money against time
    def plot_money_monthly(self):
        x_months = [m for m in range(self.sim.num_months)]
        y1_f_money = self.money["f"]
        y2_hh_money = self.money["hh"]

        fig, ax = plt.subplots()
        ax.plot(x_months, y1_f_money, 'r', label='Firms')
        ax.plot(x_months, y2_hh_money, 'b', label='Households')

        ax.set(xlabel='Months', ylabel='Money',
            title='Household and Firm Money')
        ax.grid()
        ax.legend()

        fig.savefig("money.png")
        plt.show()


######## ######## ######## IMPORTS ######## ######## ########

from simulation import Simulation
import matplotlib
import matplotlib.pyplot as plt
import numpy as np