

# the statistician object stores data about the simulation and implements methods to visualize and further process this data
class Statistician(object):

    def __init__(self, sim: object):
        self.sim = sim

        self.f_stat = {
            
            'sum': {
                'money': []
            },

            'avg': {
                'money': [],
                'num_items': [],
                'item_price': [],
                'marginal_cost': [],
                'demand': [],
                'num_employees': [],
                'wage': [],
                'months_hiring': [],    # number of months looking for employees
            },
        }

        self.hh_stat = {

            'sum': {
                'money': []
            },
            
            'avg': {
                'money': [],
                'employment': [],   # household employment rate
                'res_wage': [],
            },

            'metric': {
                'hoover': [],
                'gini': [],
            },
        }

        self.g_stat = {

            'fix': {                # direct readings
                'tax': [],
                'ubi': [],
            }
        }

    # TODO: Implement different kinds of dotted lines for black and white suitable display
    # TODO: think about days within a month. maybe higher resolution than month plots make sense for some cases
    # TODO: Max and min for how many customers do firms have
    # TODO: error bars, box plots, violin plots are great
    # TODO: Prettier graphs https://stackoverflow.com/questions/14908576/how-to-remove-frame-from-matplotlib-pyplot-figure-vs-matplotlib-figure-frame

    ######## ######## ######## METHODS ######## ######## ########

    def calc_sum(self):
        hh_list = self.sim.hh_list
        firm_list = self.sim.firm_list

        self.hh_stat['sum']['money'].append(sum([hh.money for hh in hh_list]))
        self.f_stat['sum']['money'].append(sum([f.money for f in firm_list]))

    # calculate averages for a set of firm and household characteristics
    def calc_avg(self):
        f_list = self.sim.firm_list
        num_f = self.sim.f_param['num_firms']

        self.f_stat['avg']['money'].append(sum([f.money for f in f_list]) / num_f)
        self.f_stat['avg']['num_items'].append(sum([f.num_items for f in f_list]) / num_f)
        self.f_stat['avg']['item_price'].append(sum([f.item_price for f in f_list]) / num_f)
        self.f_stat['avg']['marginal_cost'].append(sum([f.marginal_cost for f in f_list]) / num_f)
        self.f_stat['avg']['demand'].append(sum([f.demand for f in f_list]) / num_f)
        self.f_stat['avg']['num_employees'].append(sum([len(f.list_employees) for f in f_list]) / num_f)
        self.f_stat['avg']['wage'].append(sum([f.wage for f in f_list]) / num_f)
        self.f_stat['avg']['months_hiring'].append(sum([self.sim.current_month - f.month_hiring for f in f_list]) / num_f)

        hh_list = self.sim.hh_list
        num_hh = self.sim.hh_param['num_hh']

        self.hh_stat['avg']['money'].append(self.hh_stat['sum']['money'][-1] / num_hh)
        self.hh_stat['avg']['employment'].append(sum([1 if hh.employer else 0 for hh in hh_list]) / num_hh)
        self.hh_stat['avg']['res_wage'].append(sum([hh.res_wage for hh in hh_list]) / num_hh)
    
    def calc_metric(self):
        self.hh_stat['metric']['hoover'].append(self.calc_hoover())
        self.hh_stat['metric']['gini'].append(self.calc_gini())

    def calc_gov(self):
        self.g_stat['fix']['tax'].append(self.sim.gov.tax_rate)
        self.g_stat['fix']['ubi'].append(self.sim.gov.ubi)

    # calculate the hoover index as defined on https://wikimedia.org/api/rest_v1/media/math/render/svg/3e117654142eaec6efa377da812394d213955db4
    # from https://en.wikipedia.org/wiki/Hoover_index
    def calc_hoover(self):
        sum_diff_i_mean = 0
        for hh in self.sim.hh_list:
            sum_diff_i_mean += abs(hh.money - self.hh_stat['avg']['money'][-1])
        return 1/2 * sum_diff_i_mean / self.hh_stat['sum']['money'][-1]


    # based on https://github.com/oliviaguest/gini
    def calc_gini(self):
        array = np.array([hh.money for hh in self.sim.hh_list])
        # All values are treated equally, arrays must be 1d:
        array = array.flatten()
        if np.amin(array) < 0:
            # Values cannot be negative:
            array -= np.amin(array)
        # Values cannot be 0:
        array += 0.0000001
        # Values must be sorted:
        array = np.sort(array)
        # Index per array element:
        index = np.arange(1,array.shape[0]+1)
        # Number of array elements:
        n = array.shape[0]
        # Gini coefficient:
        return ((np.sum((2 * index - n  - 1) * array)) / (n * np.sum(array)))

    # each month notify the statistician of what is going on in the simulation
    def up_stat(self):
        self.calc_sum()
        self.calc_avg()
        self.calc_metric()
        if self.sim.gov_exists() is True:
            self.calc_gov()

    def plot_equality(self):
        x_months = [m for m in range(self.sim.num_months)]
        y1_hoover = self.hh_stat['metric']['hoover']
        y2_gini = self.hh_stat['metric']['gini']

        fig, ax = plt.subplots()
        ax.plot(x_months, y1_hoover, 'r', label='Hoover index')
        ax.plot(x_months, y2_gini, 'b', label='Gini index')

        ax.set(xlabel='Months', ylabel='Equality', title='Metrics of economic equality')
        ax.grid()
        ax.legend()
        fig.savefig('fig_equality.png')
        plt.show()

    # plot averages for firm money and household money against time
    def plot_money (self):
        x_months = [m for m in range(self.sim.num_months)]
        y1_f_money = self.f_stat['avg']['money']
        y2_hh_money = self.hh_stat['avg']['money']

        fig, ax = plt.subplots()
        ax.plot(x_months, y1_f_money, 'r', label='Money firm average')
        ax.plot(x_months, y2_hh_money, 'b', label='Money household average')

        ax.set(xlabel='Months', ylabel='Money', title='Money distribution between firms and households')
        ax.grid()
        ax.legend()
        fig.savefig('fig_money.png')
        plt.show()

    # plot averages for firm wage and household reservation wage against time
    def plot_wage (self):
        x_months = [m for m in range(self.sim.num_months)]
        y1_f_wage = self.f_stat['avg']['wage']
        y2_hh_res_wage = self.hh_stat['avg']['res_wage']

        fig, ax = plt.subplots()
        ax.plot(x_months, y1_f_wage, 'r', label='Wage firm average')
        ax.plot(x_months, y2_hh_res_wage, 'b', label='Reservation wage household average')

        ax.set(xlabel='Months', ylabel='Money', title='Wage and reservation wage')
        ax.grid()
        ax.legend()
        fig.savefig('fig_wage.png')
        plt.show()

    # plot averages for number of items a firm has in stock and demand 
    def plot_demand (self):
        x_months = [m for m in range(self.sim.num_months)]
        y1_f_num_items = self.f_stat['avg']['num_items']
        y2_f_demand = self.f_stat['avg']['demand']

        fig, ax = plt.subplots()
        ax.plot(x_months, y1_f_num_items, 'r', label='Number of stocked items firm average')
        ax.plot(x_months, y2_f_demand, 'b', label='Demand firm average')

        ax.set(xlabel='Months', ylabel='Items', title='Item demand and price')
        ax.grid()
        ax.legend()
        fig.savefig('fig_items.png')
        plt.show()

    # plot firm's marginal cost and item price as well as household employment rate
    def plot_items (self):
        x_months = [m for m in range(self.sim.num_months)]
        y1_f_marginal_cost = self.f_stat['avg']['marginal_cost']
        y2_f_item_price = self.f_stat['avg']['item_price']
        y3_hh_employment = self.hh_stat['avg']['employment']

        fig, ax = plt.subplots()
        ax.plot(x_months, y1_f_marginal_cost, 'b', label='Marginal cost firm average')
        ax.plot(x_months, y2_f_item_price, 'g', label='Item price firm average')
        ax.plot(x_months, y3_hh_employment, 'r', label='Employment rate of households')

        ax.set(xlabel='Months', ylabel='', title='Item price, marginal cost and employment rate')
        ax.grid()
        ax.legend()
        fig.savefig('fig_items2.png')
        plt.show()

    # plot averages for
        # firms' number of employees
        # the duration for which firms have been looking to hire
    def plot_connections (self):
        x_months = [m for m in range(self.sim.num_months)]
        y1_f_num_employees = self.f_stat['avg']['num_employees']
        y2_f_months_hiring = self.f_stat['avg']['months_hiring']

        fig, ax = plt.subplots()
        ax.plot(x_months, y1_f_num_employees, 'r', label='Number of employees firm average')
        ax.plot(x_months, y2_f_months_hiring, 'b', label='Recruiting duration firm average')

        ax.set(xlabel='Months', ylabel='', title='Employer-employee relations')
        ax.grid()
        ax.legend()
        fig.savefig('fig_connections.png')
        plt.show()

    def plot_gov1(self):
        x_months = [m for m in range(self.sim.num_months)]
        y1_tax = self.g_stat['fix']['tax']

        fig, ax = plt.subplots()
        ax.plot(x_months, y1_tax, 'r', label='Tax rate')

        ax.set(xlabel='Months', ylabel='Tax rate', title='Taxation')
        ax.grid()
        ax.legend()
        fig.savefig('fig_tax.png')
        plt.show()

    def plot_gov2(self):
        x_months = [m for m in range(self.sim.num_months)]
        y1_ubi = self.g_stat['fix']['ubi']

        fig, ax = plt.subplots()
        ax.plot(x_months, y1_ubi, 'r', label='UBI')

        ax.set(xlabel='Months', ylabel='Money', title='Universal Basic Income')
        ax.grid()
        ax.legend()
        fig.savefig('fig_ubi.png')
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

    def invoke_plots(self):
        self.plot_equality()
        self.plot_money()
        self.plot_wage()
        self.plot_demand()
        self.plot_items()
        self.plot_connections()
        if self.sim.gov_exists() is True:
            self.plot_gov1()
            self.plot_gov2()
        self.hist_money()

######## ######## ######## IMPORTS ######## ######## ########

from simulation import Simulation
import matplotlib
import matplotlib.pyplot as plt
import numpy as np