

from stat_plot import Stat_plot
from simulation import Simulation
import numpy as np

class Stat_run(Stat_plot):
    '''
    The stat_run object stores and processes data about a single simulation run.
    It inherits methods to visualize this data.
    '''

    ######## ######## ######## CONSTRUCTOR ######## ######## ########

    def __init__(self, sim: object):
        self.sim = sim
        self.x_months = [m for m in range(self.sim.num_months)]     # x-axis for most plots is time in months

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
                'parties': [],      # representative government's party composition over time
            }
        }

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
        if self.sim.gov_type == 'rep': self.g_stat['fix']['parties'].append(self.sim.gov.party_size)

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

    # each month notify stat_run of what is going on in the simulation
    def up_stat(self):
        self.calc_sum()
        self.calc_avg()
        self.calc_metric()
        if self.sim.gov_exists() is True:
            self.calc_gov()

    # invoke the appropriate plots given the configuration of the simulation
    def invoke_plots(self):
        self.plot_equality()
        self.plot_money()
        self.plot_wage()
        self.plot_demand()
        self.plot_items()
        self.plot_connections()
        if self.sim.gov_exists() is True:
            self.plot_tax()
            self.plot_ubi()
            if self.sim.gov_type == 'rep':
                self.plot_parties()
        self.hist_money()

######## ######## ######## TODOS ######## ######## ########

    # TODO: Implement different kinds of dotted lines for black and white suitable display
    # TODO: think about days within a month. maybe higher resolution than month plots make sense for some cases
    # TODO: Max and min for how many customers do firms have
    # TODO: error bars, box plots, violin plots are great
    # TODO: Prettier graphs https://stackoverflow.com/questions/14908576/how-to-remove-frame-from-matplotlib-pyplot-figure-vs-matplotlib-figure-frame
    
    # TODO: Indication for movement between quantiles in firms and households.