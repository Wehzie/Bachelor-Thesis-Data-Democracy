

from statistician import Statistician
from simulation import Simulation
import numpy as np

class Stat_run(Statistician):
    '''
    The stat_run object stores and processes data about a single simulation run.
    It inherits methods to visualize this data.
    '''

    ######## ######## ######## METHODS ######## ######## ########

    # distribution measures
    def calc_dist(self):
        self.f_stat['dist']['money'] = np.append(self.f_stat['dist']['money'], [f.money for f in self.sim.firm_list])
        self.f_stat['dist']['wage'] = np.append(self.f_stat['dist']['wage'], [f.wage for f in self.sim.firm_list])
        self.hh_stat['dist']['money'] = np.append(self.hh_stat['dist']['money'], [hh.money for hh in self.sim.hh_list])
        self.hh_stat['dist']['income'] = np.append(self.hh_stat['dist']['income'], [hh.income for hh in self.sim.hh_list])

    # sum measures
    def calc_sum(self):
        hh_list = self.sim.hh_list
        firm_list = self.sim.firm_list

        self.hh_stat['sum']['money'] = np.append(self.hh_stat['sum']['money'], sum([hh.money for hh in hh_list]))
        self.f_stat['sum']['money'] = np.append(self.f_stat['sum']['money'], sum([f.money for f in firm_list]))

    # calculate averages for a set of firm and household characteristics
    def calc_avg(self):
        f_list = self.sim.firm_list
        num_f = self.sim.f_param['num_firms']

        self.f_stat['avg']['money'] = np.append(self.f_stat['avg']['money'], self.f_stat['sum']['money'][-1] / num_f)
        self.f_stat['avg']['num_items'] = np.append(self.f_stat['avg']['num_items'], sum([f.num_items for f in f_list]) / num_f)
        self.f_stat['avg']['item_price'] = np.append(self.f_stat['avg']['item_price'], sum([f.item_price for f in f_list]) / num_f)
        self.f_stat['avg']['marginal_cost'] = np.append(self.f_stat['avg']['marginal_cost'], sum([f.marginal_cost for f in f_list]) / num_f)
        self.f_stat['avg']['demand'] = np.append(self.f_stat['avg']['demand'], sum([f.demand for f in f_list]) / num_f)
        self.f_stat['avg']['num_employees'] = np.append(self.f_stat['avg']['num_employees'], sum([len(f.list_employees) for f in f_list]) / num_f)
        self.f_stat['avg']['wage'] = np.append(self.f_stat['avg']['wage'], sum([f.wage for f in f_list]) / num_f)
        self.f_stat['avg']['months_hiring'] = np.append(self.f_stat['avg']['months_hiring'], sum([self.sim.current_month - f.month_hiring for f in f_list]) / num_f)

        hh_list = self.sim.hh_list
        num_hh = self.sim.hh_param['num_hh']

        self.hh_stat['avg']['money'] = np.append(self.hh_stat['avg']['money'], self.hh_stat['sum']['money'][-1] / num_hh)
        self.hh_stat['avg']['income'] = np.append(self.hh_stat['avg']['income'], sum([hh.income for hh in hh_list]) / num_hh)
        self.hh_stat['avg']['employment'] = np.append(self.hh_stat['avg']['employment'], sum([1 if hh.employer else 0 for hh in hh_list]) / num_hh)
        self.hh_stat['avg']['res_wage'] = np.append(self.hh_stat['avg']['res_wage'], sum([hh.res_wage for hh in hh_list]) / num_hh)
    
    # calculate equality metrics
    def calc_metric(self):
        self.hh_stat['metric']['gini_m'] = np.append(self.hh_stat['metric']['gini_m'], self.calc_gini('money'))
        self.hh_stat['metric']['gini_i'] = np.append(self.hh_stat['metric']['gini_i'], self.calc_gini('income'))

    # calculate government metrics
    def calc_gov(self):
        self.g_stat['fix']['tax'] = np.append(self.g_stat['fix']['tax'], self.sim.gov.tax_rate)
        self.g_stat['fix']['ubi'] = np.append(self.g_stat['fix']['ubi'], self.sim.gov.ubi)
        if self.gov_type == 'rep':
            self.g_stat['fix']['parties'] = np.append(self.g_stat['fix']['parties'], self.sim.gov.parties)

    # calculate Gini index/coefficient
    # based on https://github.com/oliviaguest/gini
    # Guest, O., & Love, B. C. (2017). What the Success of Brain Imaging Implies about the Neural Code. eLife. doi: 10.7554/eLife.21397.
    def calc_gini(self, g_type):
        if g_type == 'income': array = np.array([hh.income for hh in self.sim.hh_list])
        if g_type == 'money': array = np.array([hh.money for hh in self.sim.hh_list])
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

    # each month notify stat_run of occurrences in the simulation
    def up_stat(self):
        if self.sim.current_month == self.sim.num_months-1:     # in the last month of a run store income and money distribution for histograms
            self.calc_dist()
        self.calc_sum()
        self.calc_avg()
        self.calc_metric()
        if self.gov_type != 'none':
            self.calc_gov()

