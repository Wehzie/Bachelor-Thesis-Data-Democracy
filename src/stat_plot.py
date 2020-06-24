

import matplotlib.pyplot as plt
import numpy as np
from collections import deque

class Stat_plot(object):
    '''
    The stat_plot class is abstract and not instantiated it inherits plotting capabilities.
    '''

    def plot_equality(self):
        y1_hoover = self.hh_stat['metric']['hoover']
        y2_gini = self.hh_stat['metric']['gini']

        fig, ax = plt.subplots()
        ax.plot(self.x_months, y1_hoover, 'r', label='Hoover index')
        ax.plot(self.x_months, y2_gini, 'b', label='Gini index')

        ax.set(xlabel='Months', ylabel='Equality', title='Metrics of economic equality')
        ax.grid()
        ax.legend()
        fig.savefig('fig_equality.png')
        plt.show()

    # plot averages for firm money and household money against time
    def plot_money (self):
        y1_f_money = self.f_stat['avg']['money']
        y2_hh_money = self.hh_stat['avg']['money']

        fig, ax = plt.subplots()
        ax.plot(self.x_months, y1_f_money, 'r', label='Money firm average')
        ax.plot(self.x_months, y2_hh_money, 'b', label='Money household average')

        ax.set(xlabel='Months', ylabel='Money', title='Money distribution between firms and households')
        ax.grid()
        ax.legend()
        fig.savefig('fig_money.png')
        plt.show()

    # plot averages for firm wage and household reservation wage against time
    def plot_wage (self):
        y1_f_wage = self.f_stat['avg']['wage']
        y2_hh_res_wage = self.hh_stat['avg']['res_wage']

        fig, ax = plt.subplots()
        ax.plot(self.x_months, y1_f_wage, 'r', label='Wage firm average')
        ax.plot(self.x_months, y2_hh_res_wage, 'b', label='Reservation wage household average')

        ax.set(xlabel='Months', ylabel='Money', title='Wage and reservation wage')
        ax.grid()
        ax.legend()
        fig.savefig('fig_wage.png')
        plt.show()

    # plot averages for number of items a firm has in stock and demand 
    def plot_demand (self):
        y1_f_num_items = self.f_stat['avg']['num_items']
        y2_f_demand = self.f_stat['avg']['demand']

        fig, ax = plt.subplots()
        ax.plot(self.x_months, y1_f_num_items, 'r', label='Number of stocked items firm average')
        ax.plot(self.x_months, y2_f_demand, 'b', label='Demand firm average')

        ax.set(xlabel='Months', ylabel='Items', title='Item demand and price')
        ax.grid()
        ax.legend()
        fig.savefig('fig_items.png')
        plt.show()

    # plot firm's marginal cost and item price as well as household employment rate
    def plot_items (self):
        y1_f_marginal_cost = self.f_stat['avg']['marginal_cost']
        y2_f_item_price = self.f_stat['avg']['item_price']
        y3_hh_employment = self.hh_stat['avg']['employment']

        fig, ax = plt.subplots()
        ax.plot(self.x_months, y1_f_marginal_cost, 'b', label='Marginal cost firm average')
        ax.plot(self.x_months, y2_f_item_price, 'g', label='Item price firm average')
        ax.plot(self.x_months, y3_hh_employment, 'r', label='Employment rate of households')

        ax.set(xlabel='Months', ylabel='', title='Item price, marginal cost and employment rate')
        ax.grid()
        ax.legend()
        fig.savefig('fig_items2.png')
        plt.show()

    # plot averages for
        # firms' number of employees
        # the duration for which firms have been looking to hire
    def plot_connections (self):
        y1_f_num_employees = self.f_stat['avg']['num_employees']
        y2_f_months_hiring = self.f_stat['avg']['months_hiring']

        fig, ax = plt.subplots()
        ax.plot(self.x_months, y1_f_num_employees, 'r', label='Number of employees firm average')
        ax.plot(self.x_months, y2_f_months_hiring, 'b', label='Recruiting duration firm average')

        ax.set(xlabel='Months', ylabel='', title='Employer-employee relations')
        ax.grid()
        ax.legend()
        fig.savefig('fig_connections.png')
        plt.show()

    # plot the tax rate set by government for each month
    def plot_tax(self):
        y1_tax = self.g_stat['fix']['tax']

        fig, ax = plt.subplots()
        ax.plot(self.x_months, y1_tax, 'r', label='Tax rate')

        ax.set(xlabel='Months', ylabel='Tax rate', title='Taxation')
        ax.grid()
        ax.legend()
        fig.savefig('fig_tax.png')
        plt.show()

    # plot the universal basic income set by government for each month
    def plot_ubi(self):
        y1_ubi = self.g_stat['fix']['ubi']

        fig, ax = plt.subplots()
        ax.plot(self.x_months, y1_ubi, 'r', label='UBI')

        ax.set(xlabel='Months', ylabel='Money', title='Universal Basic Income')
        ax.grid()
        ax.legend()
        fig.savefig('fig_ubi.png')
        plt.show()

    # plot the party composition of the representative government for each month
    def plot_parties(self):
        parties = deque(self.g_stat['fix']['parties'])
        y1_party, y2_party, y3_party, y4_party, y5_party = ([] for i in range(5))
        for i in range(len(parties)//5):
            y1_party.append(parties.popleft())
            y2_party.append(parties.popleft())
            y3_party.append(parties.popleft())
            y4_party.append(parties.popleft())
            y5_party.append(parties.popleft())

        fig, ax = plt.subplots()
        ax.plot(self.x_months, y1_party, 'r', label='Party quintile 1')     # party representing the poorest quintile of hhs
        ax.plot(self.x_months, y2_party, 'g', label='Party quintile 2')
        ax.plot(self.x_months, y3_party, 'b', label='Party quintile 3')
        ax.plot(self.x_months, y4_party, 'k', label='Party quintile 4')
        ax.plot(self.x_months, y5_party, 'c', label='Party quintile 5')

        ax.set(xlabel='Months', ylabel='Party size', title='Party composition')
        ax.grid()
        ax.legend()
        fig.savefig('fig_parties.png')
        plt.show()

    def hist_money(self):
        # money distribution at the end of the simulation
        f_money_list = [f.money for f in self.sim.firm_list]
        hh_money_list = [hh.money for hh in self.sim.hh_list]

        fig, (ax1, ax2) = plt.subplots(1, 2)
        ax1.hist(f_money_list, bins=int(self.sim.f_param['num_firms']/10))
        ax2.hist(hh_money_list, bins=int(self.sim.hh_param['num_hh']/10))

        fig.suptitle("Money distribution within households and firms")
        ax1.set(xlabel='Money', ylabel='Number of firms')
        ax1.grid()
        ax2.set(xlabel='Money', ylabel='Number of households')
        ax2.grid()
        fig.savefig('fig_hist_money.png')
        plt.show()