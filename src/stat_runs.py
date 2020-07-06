

from simulation import Simulation
from statistician import Statistician
from collections import deque
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

class Stat_runs(Statistician):
    '''
    The stat_runs object stores stat_run objects generated from multiple runs.
    The data in the stat_run objects is analyzed and plotted.
    '''

    ######## ######## ######## METHODS ######## ######## ########

    def add_run(self, run: object):
        for stat_key, stat_val in run.f_stat.items():
            for measure_key, measure_val in stat_val.items():
                self.f_stat[stat_key][measure_key] = np.vstack((self.f_stat[stat_key][measure_key], np.array(measure_val)))

        for stat_key, stat_val in run.hh_stat.items():
            for measure_key, measure_val in stat_val.items():
                self.hh_stat[stat_key][measure_key] = np.vstack((self.hh_stat[stat_key][measure_key], np.array(measure_val)))

        if self.gov_type != 'none':
            for stat_key, stat_val in run.g_stat.items():
                for measure_key, measure_val in stat_val.items():
                    if len(measure_val) == 0: continue                  # only add party data for the representative government
                    self.g_stat[stat_key][measure_key] = np.vstack((self.g_stat[stat_key][measure_key], np.array(measure_val)))
        
    ######## ######## ######## MULTIPLE RUN PLOTS ######## ######## ########

    # plot the gini and hover indices of economic equality against time
    def plot_equality(self):
        y1_hoover = np.mean(self.hh_stat['metric']['hoover'], axis=0)
        y2_gini = np.mean(self.hh_stat['metric']['gini'], axis=0)
        e1 = stats.sem(self.hh_stat['metric']['hoover'])
        e2 = stats.sem(self.hh_stat['metric']['gini'])

        fig, ax = plt.subplots()
        plt.errorbar(self.x_months, y1_hoover, e1, color='r', label='Hoover index')
        plt.errorbar(self.x_months, y2_gini, e2, color='b', label='Gini index')

        ax.set(xlabel='Months', ylabel='Equality', title='Metrics of economic equality')
        ax.grid()
        ax.legend()
        if self.plot_param['save_pgf']: fig.savefig('img/fig_' + self.gov_type + '_equality.pgf')
        if self.plot_param['save_pdf']: fig.savefig('img/fig_' + self.gov_type + '_equality.pdf')
        if self.plot_param['save_png']: fig.savefig('img/fig_' + self.gov_type + '_equality.png', dpi=300)
        if self.plot_param['show_plots']: plt.show()

    # plot averages for firm money and household money against time
    def plot_money(self):
        y1_f_money = np.mean(self.f_stat['avg']['money'], axis=0)
        y2_hh_money = np.mean(self.hh_stat['avg']['money'], axis=0)
        e1 = stats.sem(self.f_stat['avg']['money'])
        e2 = stats.sem(self.hh_stat['avg']['money'])

        fig, ax = plt.subplots()
        plt.errorbar(self.x_months, y1_f_money, e1, color='r', label='Money firm average')
        plt.errorbar(self.x_months, y2_hh_money, e2, color='b', label='Money household average')

        ax.set(xlabel='Months', ylabel='Money', title='Money distribution between firms and households')
        ax.grid()
        ax.legend()
        if self.plot_param['save_pgf']: fig.savefig('img/fig_'+ self.gov_type +'_money.pgf')
        if self.plot_param['save_pdf']: fig.savefig('img/fig_'+ self.gov_type +'_money.pdf')
        if self.plot_param['save_png']: fig.savefig('img/fig_'+ self.gov_type +'_money.png', dpi=300)
        if self.plot_param['show_plots']: plt.show()

    # plot averages for firm wage and household reservation wage against time
    def plot_wage(self):
        y1_f_wage = np.mean(self.f_stat['avg']['wage'], axis=0)
        y2_hh_res_wage = np.mean(self.hh_stat['avg']['res_wage'], axis=0)
        e1 = stats.sem(self.f_stat['avg']['wage'])
        e2 = stats.sem(self.hh_stat['avg']['res_wage'])

        fig, ax = plt.subplots()
        plt.errorbar(self.x_months, y1_f_wage, e1, color='r', label='Wage firm average')
        plt.errorbar(self.x_months, y2_hh_res_wage, e2, color='b', label='Reservation wage household average')

        ax.set(xlabel='Months', ylabel='Money', title='Wage and reservation wage')
        ax.grid()
        ax.legend()
        if self.plot_param['save_pgf']: fig.savefig('img/fig_'+ self.gov_type +'_wage.pgf')
        if self.plot_param['save_pdf']: fig.savefig('img/fig_'+ self.gov_type +'_wage.pdf')
        if self.plot_param['save_png']: fig.savefig('img/fig_'+ self.gov_type +'_wage.png', dpi=300)
        if self.plot_param['show_plots']: plt.show()

    # plot averages for number of items a firm has in stock and demand 
    def plot_demand(self):
        y1_f_num_items = np.mean(self.f_stat['avg']['num_items'], axis=0)
        y2_f_demand = np.mean(self.f_stat['avg']['demand'], axis=0)
        e1 = stats.sem(self.f_stat['avg']['num_items'])
        e2 = stats.sem(self.f_stat['avg']['demand'])

        fig, ax = plt.subplots()
        plt.errorbar(self.x_months, y1_f_num_items, e1, color='r', label='Number of stocked items firm average')
        plt.errorbar(self.x_months, y2_f_demand, e2, color='b', label='Demand firm average')

        ax.set(xlabel='Months', ylabel='Items', title='Item demand and price')
        ax.grid()
        ax.legend()
        if self.plot_param['save_pgf']: fig.savefig('img/fig_'+ self.gov_type +'_demand.pgf')
        if self.plot_param['save_pdf']: fig.savefig('img/fig_'+ self.gov_type +'_demand.pdf')
        if self.plot_param['save_png']: fig.savefig('img/fig_'+ self.gov_type +'_demand.png', dpi=300)
        if self.plot_param['show_plots']: plt.show()

    # plot firm's marginal cost and item price
    def plot_item_cost(self):
        y1_f_marginal_cost = np.mean(self.f_stat['avg']['marginal_cost'], axis=0)
        y2_f_item_price = np.mean(self.f_stat['avg']['item_price'], axis=0)
        e1 = stats.sem(self.f_stat['avg']['marginal_cost'])
        e2 = stats.sem(self.f_stat['avg']['item_price'])

        fig, ax = plt.subplots()
        plt.errorbar(self.x_months, y1_f_marginal_cost, e1, color='b', label='Marginal cost firm average')
        plt.errorbar(self.x_months, y2_f_item_price, e2, color='g', label='Item price firm average')

        ax.set(xlabel='Months', ylabel='', title='Item price and marginal cost')
        ax.grid()
        ax.legend()
        if self.plot_param['save_pgf']: fig.savefig('img/fig_'+ self.gov_type +'_item_cost.pgf')
        if self.plot_param['save_pdf']: fig.savefig('img/fig_'+ self.gov_type +'_item_cost.pdf')
        if self.plot_param['save_png']: fig.savefig('img/fig_'+ self.gov_type +'_item_cost.png', dpi=300)
        if self.plot_param['show_plots']: plt.show()
    
    # plot household employment rate
    def plot_employment(self):
        y1_hh_employment = np.mean(self.hh_stat['avg']['employment'], axis=0)
        e1 = stats.sem(self.hh_stat['avg']['employment'])

        fig, ax = plt.subplots()
        plt.errorbar(self.x_months, y1_hh_employment, e1, color='b', label='Employment rate')

        ax.set(xlabel='Months', ylabel='', title='Household employment rate')
        ax.grid()
        ax.legend()
        if self.plot_param['save_pgf']: fig.savefig('img/fig_'+ self.gov_type +'_employment.pgf')
        if self.plot_param['save_pdf']: fig.savefig('img/fig_'+ self.gov_type +'_employment.pdf')
        if self.plot_param['save_png']: fig.savefig('img/fig_'+ self.gov_type +'_employment.png', dpi=300)
        if self.plot_param['show_plots']: plt.show()

    # plot averages for
        # firms' number of employees
        # the duration for which firms have been looking to hire
    def plot_connections(self):
        y1_f_num_employees = np.mean(self.f_stat['avg']['num_employees'], axis=0)
        y2_f_months_hiring = np.mean(self.f_stat['avg']['months_hiring'], axis=0)
        e1 = stats.sem(self.f_stat['avg']['num_employees'])
        e2 = stats.sem(self.f_stat['avg']['months_hiring'])

        fig, ax = plt.subplots()
        plt.errorbar(self.x_months, y1_f_num_employees, e1, color='r', label='Number of employees firm average')
        plt.errorbar(self.x_months, y2_f_months_hiring, e2, color='b', label='Recruiting duration firm average')

        ax.set(xlabel='Months', ylabel='', title='Employer-employee relations')
        ax.grid()
        ax.legend()
        if self.plot_param['save_pgf']: fig.savefig('img/fig_'+ self.gov_type +'_connections.pgf')
        if self.plot_param['save_pdf']: fig.savefig('img/fig_'+ self.gov_type +'_connections.pdf')
        if self.plot_param['save_png']: fig.savefig('img/fig_'+ self.gov_type +'_connections.png', dpi=300)
        if self.plot_param['show_plots']: plt.show()

    # plot the tax rate set by government for each month
    def plot_tax(self):
        y1_tax = np.mean(self.g_stat['fix']['tax'], axis=0)
        e1 = stats.sem(self.g_stat['fix']['tax'])

        fig, ax = plt.subplots()
        plt.errorbar(self.x_months, y1_tax, e1, color='r', label='Tax rate')

        ax.set(xlabel='Months', ylabel='Tax rate', title='Taxation')
        ax.grid()
        ax.legend()
        if self.plot_param['save_pgf']: fig.savefig('img/fig_'+ self.gov_type +'_tax.pgf')
        if self.plot_param['save_pdf']: fig.savefig('img/fig_'+ self.gov_type +'_tax.pdf')
        if self.plot_param['save_png']: fig.savefig('img/fig_'+ self.gov_type +'_tax.png', dpi=300)
        if self.plot_param['show_plots']: plt.show()

    # plot the universal basic income set by government for each month
    def plot_ubi(self):
        y1_ubi = np.mean(self.g_stat['fix']['ubi'], axis=0)
        e1 = stats.sem(self.g_stat['fix']['ubi'])

        fig, ax = plt.subplots()
        plt.errorbar(self.x_months, y1_ubi, e1, color='r', label='UBI')

        ax.set(xlabel='Months', ylabel='Money', title='Universal Basic Income')
        ax.grid()
        ax.legend()
        if self.plot_param['save_pgf']: fig.savefig('img/fig_'+ self.gov_type +'_ubi.pgf')
        if self.plot_param['save_pdf']: fig.savefig('img/fig_'+ self.gov_type +'_ubi.pdf')
        if self.plot_param['save_png']: fig.savefig('img/fig_'+ self.gov_type +'_ubi.png', dpi=300)
        if self.plot_param['show_plots']: plt.show()

    # plot the party composition of the representative government for each month
    def plot_parties(self):
        parties = self.g_stat['fix']['parties']
        y1_party, y2_party, y3_party, y4_party, y5_party = (np.empty((0, self.sim.num_months)) for i in range(5))
        p_list = [y1_party, y2_party, y3_party, y4_party, y5_party]

        for row in range(np.size(parties, 0)):
            col = 0
            y1_col, y2_col, y3_col, y4_col, y5_col = (np.empty(0) for i in range(5))
            while col < np.size(parties, 1):
                y1_col = np.append(y1_col, parties[row][col])
                y2_col = np.append(y2_col, parties[row][col+1])
                y3_col = np.append(y3_col, parties[row][col+2])
                y4_col = np.append(y4_col, parties[row][col+3])
                y5_col = np.append(y5_col, parties[row][col+4])
                col += 5
            y1_party = np.vstack((y1_party, y1_col))
            y2_party = np.vstack((y2_party, y2_col))
            y3_party = np.vstack((y3_party, y3_col))
            y4_party = np.vstack((y4_party, y4_col))
            y5_party = np.vstack((y5_party, y5_col))
        
        e1 = stats.sem(y1_party)
        e2 = stats.sem(y2_party)
        e3 = stats.sem(y3_party)
        e4 = stats.sem(y4_party)
        e5 = stats.sem(y5_party)

        y1_party = np.mean(y1_party, axis=0)
        y2_party = np.mean(y2_party, axis=0)
        y3_party = np.mean(y3_party, axis=0)
        y4_party = np.mean(y4_party, axis=0)
        y5_party = np.mean(y5_party, axis=0)

        fig, ax = plt.subplots()
        plt.errorbar(self.x_months, y1_party, e1, color='r', label='Party quintile 1')     # party representing the poorest quintile of hhs
        plt.errorbar(self.x_months, y2_party, e2, color='g', label='Party quintile 2')
        plt.errorbar(self.x_months, y3_party, e3, color='b', label='Party quintile 3')
        plt.errorbar(self.x_months, y4_party, e4, color='k', label='Party quintile 4')
        plt.errorbar(self.x_months, y5_party, e5, color='c', label='Party quintile 5')

        ax.set(xlabel='Months', ylabel='Party size', title='Party composition')
        ax.grid()
        ax.legend()
        if self.plot_param['save_pgf']: fig.savefig('img/fig_'+ self.gov_type +'_parties.pgf')
        if self.plot_param['save_pdf']: fig.savefig('img/fig_'+ self.gov_type +'_parties.pdf')
        if self.plot_param['save_png']: fig.savefig('img/fig_'+ self.gov_type +'_parties.png', dpi=300)
        if self.plot_param['show_plots']: plt.show()

    # money distribution at the end of the simulation
    def hist_money(self):
        f_money_list = (self.f_stat['dist']['money']).flatten()
        hh_money_list = (self.hh_stat['dist']['money']).flatten()

        fig, (ax1, ax2) = plt.subplots(1, 2)
        ax1.hist(f_money_list, bins=int(self.sim.f_param['num_firms']/10))
        ax2.hist(hh_money_list, bins=int(self.sim.hh_param['num_hh']/10))

        fig.suptitle("Money distribution within households and firms")
        ax1.set(xlabel='Money', ylabel='Number of firms')
        ax1.grid()
        ax2.set(xlabel='Money', ylabel='Number of households')
        ax2.grid()
        if self.plot_param['save_pgf']: fig.savefig('img/fig_'+ self.gov_type +'_hist_money.pgf')
        if self.plot_param['save_pdf']: fig.savefig('img/fig_'+ self.gov_type +'_hist_money.pdf')
        if self.plot_param['save_png']: fig.savefig('img/fig_'+ self.gov_type +'_hist_money.png', dpi=300)
        if self.plot_param['show_plots']: plt.show()