

# the statistician object stores data about the simulation and implements methods to visualize and further process this data
class Statistician(object):

    def __init__(self, sim: object):
        self.sim = sim

        # TODO: For now averages are stored, consider splitting up for further statistics, e.G. median, spreads etc.
        self.f_stat = {

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
                'employment': [],   # number employed households, normalized
                'num_vendors': [],
                'res_wage': [],
            },

            'metric': {
                'hoover': [],
                'gini': [],
            },
        }

    # TODO: Implement different kinds of dotted lines for black and white suitable display
    # TODO: think about days within a month. maybe higher resolution than month plots make sense for some cases
    # TODO: Max and min for how many customers do firms have

    ######## ######## ######## METHODS ######## ######## ########

    def calc_sum(self):
        hh_list = self.sim.hh_list

        self.hh_stat['sum']['money'].append(sum([hh.money for hh in hh_list]))
        #TODO: confirm overall money is constant

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
        self.hh_stat['avg']['num_vendors'].append(sum([len(hh.vendor_list) for hh in hh_list]) / num_hh)
        self.hh_stat['avg']['res_wage'].append(sum([hh.res_wage for hh in hh_list]) / num_hh)
    
    def calc_metric(self):
        self.hh_stat['metric']['hoover'].append(self.calc_hoover())
        self.hh_stat['metric']['gini'].append(self.calc_gini())

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

    # plot averages for firm wage, firm marginal cost and household reservation wage against time
    def plot_wage (self):
        x_months = [m for m in range(self.sim.num_months)]
        y1_f_wage = self.f_stat['avg']['wage']
        #y2_f_marginal_cost = self.f_stat['avg']['marginal_cost']
        y3_hh_res_wage = self.hh_stat['avg']['res_wage']

        fig, ax = plt.subplots()
        ax.plot(x_months, y1_f_wage, 'r', label='Wage firm average')
        #ax.plot(x_months, y2_f_marginal_cost, 'b', label='Marginal cost firm average')
        ax.plot(x_months, y3_hh_res_wage, 'g', label='Reservation wage household average')

        ax.set(xlabel='Months', ylabel='Money', title='Wages and marginal cost')
        ax.grid()
        ax.legend()

        fig.savefig('fig_wage.png')
        plt.show()

    def plot_items2 (self):
        x_months = [m for m in range(self.sim.num_months)]
        y1_f_marginal_cost = self.f_stat['avg']['marginal_cost']
        y2_f_item_price = self.f_stat['avg']['item_price']

        fig, ax = plt.subplots()
        ax.plot(x_months, y1_f_marginal_cost, 'b', label='Marginal cost firm average')
        ax.plot(x_months, y2_f_item_price, 'b', label='Item price firm average')

        ax.set(xlabel='Months', ylabel='', title='Item price and marginal cost')
        ax.grid()
        ax.legend()

        fig.savefig('fig_items2.png')
        plt.show()

    # plot averages for number of items a firm has in stock, item price and demand 
    def plot_items (self):
        x_months = [m for m in range(self.sim.num_months)]
        y1_f_num_items = self.f_stat['avg']['num_items']
        y2_f_item_price = self.f_stat['avg']['item_price']
        #y3_f_demand = self.f_stat['avg']['demand']

        fig, ax = plt.subplots()
        ax.plot(x_months, y1_f_num_items, 'r', label='Number of stocked items firm average')
        ax.plot(x_months, y2_f_item_price, 'b', label='Item price firm average')
        #ax.plot(x_months, y3_f_demand, 'g', label='Demand firm average')

        ax.set(xlabel='Months', ylabel='', title='Item demand and price')
        ax.grid()
        ax.legend()

        fig.savefig('fig_items.png')
        plt.show()

    # plot averages for
        # firms' number of employees
        # the duration for which firms have been looking to hire
        # the employment rate amongst households
        # the number of vendors households buy from
    def plot_connections (self):
        x_months = [m for m in range(self.sim.num_months)]
        y1_f_num_employees = self.f_stat['avg']['num_employees']
        y2_f_months_hiring = self.f_stat['avg']['months_hiring']
        y3_hh_employment = self.hh_stat['avg']['employment']
        y4_hh_num_vendors = self.hh_stat['avg']['num_vendors']

        fig, ax = plt.subplots()
        ax.plot(x_months, y1_f_num_employees, 'r', label='Number of employees firm average')
        ax.plot(x_months, y2_f_months_hiring, 'g', label='Recruiting duration firm average')
        ax.plot(x_months, y3_hh_employment, 'b', label='Employment rate of households')                # BUG: constant at 100% (1.00)
        ax.plot(x_months, y4_hh_num_vendors, 'k', label='Vendor number household average')

        ax.set(xlabel='Months', ylabel='', title='Employment and customer-vendor connections')

        ax.grid()
        ax.legend()

        fig.savefig('fig_connections.png')
        plt.show()

    def plot_demand_hhmoney (self):
        x_months = [m for m in range(self.sim.num_months)]
        y1_f_demand = self.f_stat['avg']['demand']
        y2_hh_money = self.hh_stat['avg']['money']

        fig, ax = plt.subplots()
        ax.plot(x_months, y1_f_demand, 'r', label='Firm demand average')
        ax.plot(x_months, y2_hh_money, 'b', label='Household money average')

        ax.set(xlabel='Months', ylabel='Money', title='Firm demand and household money')
        ax.grid()
        ax.legend()

        fig.savefig('fig_demand.png')
        plt.show()

    def hist_fmoney(self):
        # money distribution at the end of the simulation
        f_money_list = []
        for f in self.sim.firm_list:
            f_money_list.append(f.money)

        fig, ax = plt.subplots()

        # We can set the number of bins with the `bins` kwarg
        ax.hist(f_money_list, bins=10)

        ax.set(xlabel='Money', ylabel='Number of firms', title='Firm money')
        ax.grid()

        fig.savefig('fig_hist_fmoney.png')
        plt.show()

    def invoke_plots(self):
        self.plot_equality()
        self.plot_money()
        self.plot_wage()
        self.plot_items2()
        self.plot_items()
        self.plot_connections()
        self.plot_demand_hhmoney()
        self.hist_fmoney()

######## ######## ######## IMPORTS ######## ######## ########

from simulation import Simulation
import matplotlib
import matplotlib.pyplot as plt
import numpy as np