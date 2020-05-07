

class Statistician(object):

    def __init__(self, sim: object):
        self.sim = sim
        self.money = {"f": [], "hh": [], "f_reserve": []}
        self.price = []
        self.wage = []
        self.employment = []

        # TODO: divide into dict with f and hh subgroups

    ######## ######## ######## METHODS ######## ######## ########

    # TODO: Move these kind of methods to simulation
    def sum_f_money(self) -> float:
        f_sum = 0
        for f in self.sim.firm_list:
            f_sum += f.money
        return f_sum
    
    def sum_f_reserve(self) -> float:
        f_sum = 0
        for f in self.sim.firm_list:
            f_sum += f.reserve
        return f_sum

    def sum_hh_money(self) -> float:
        hh_sum = 0
        for hh in self.sim.hh_list:
            hh_sum += hh.money
        return hh_sum
    
    def get_employment(self) -> float:
        num_employed = 0
        for hh in self.sim.hh_list:
            if hh.employer != None: num_employed += 1
        return num_employed / len(self.sim.hh_list)
    
    def up_stat(self):
        self.money["f"].append(self.sum_f_money())
        self.money["hh"].append(self.sum_hh_money())
        self.money["f_reserve"].append(self.sum_f_reserve())
        self.employment.append(self.get_employment())

    # TODO: think about days within a month
    # plot hh and firm money against time
    def plot_money_monthly(self):
        x_months = [m for m in range(self.sim.num_months)]
        y1_f_money = self.money["f"]
        y2_hh_money = self.money["hh"]
        y3_f_reserve = self.money["f_reserve"]

        fig, ax = plt.subplots()
        ax.plot(x_months, y1_f_money, 'r', label='Firms')
        ax.plot(x_months, y2_hh_money, 'b', label='Households')
        ax.plot(x_months, y3_f_reserve, 'g', label='Firm Reserve')

        ax.set(xlabel='Months', ylabel='Money',
            title='Household and Firm Money')
        ax.grid()
        ax.legend()

        fig.savefig("money2.png")
        plt.show()
    
    # TODO: price and wage
    # in reference to https://sim4edu.com/sims/20/index.html?lang=de
    def plot_price_wage_employment(self):
        x_months = [m for m in range(self.sim.num_months)]
        y1_employment = self.employment

        fig, ax = plt.subplots()
        ax.plot(x_months, y1_employment, 'r', label='Employment')

        ax.set(xlabel='Months', ylabel='Employment',
            title='Household Employment')
        ax.grid()
        ax.legend()

        fig.savefig("employment.png")
        plt.show()

    def invoke_plots(self):
        self.plot_money_monthly()
        self.plot_price_wage_employment()

######## ######## ######## IMPORTS ######## ######## ########

from simulation import Simulation
import matplotlib
import matplotlib.pyplot as plt
import numpy as np