

######## ######## ######## IMPORTS ######## ######## ########

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# the super statistician object stores statistician objects generated from multiple runs

class Super_stat(object):

    ######## ######## ######## CONSTRUCTOR ######## ######## ########

    def __init__(self, num_months: int):
    
        self.f_stat = {
            
            'sum': {
                'money': np.empty((0, num_months)),
            },

            'avg': {
                'money': np.empty((0, num_months)),
                'num_items': np.empty((0, num_months)),
                'item_price': np.empty((0, num_months)),
                'marginal_cost': np.empty((0, num_months)),
                'demand': np.empty((0, num_months)),
                'num_employees': np.empty((0, num_months)),
                'wage': np.empty((0, num_months)),
                'months_hiring': np.empty((0, num_months)),
            },
        }

        self.hh_stat = {

            'sum': {
                'money': np.empty((0, num_months)),
            },
            
            'avg': {
                'money': np.empty((0, num_months)),
                'employment': np.empty((0, num_months)),
                'res_wage': np.empty((0, num_months)),
            },

            'metric': {
                'hoover': np.empty((0, num_months)),
                'gini': np.empty((0, num_months)),
            },
        }

        self.g_stat = {

            'fix': {                # direct readings
                'tax': np.empty((0, num_months)),
                'ubi': np.empty((0, num_months)),
                'parties': np.empty((0, num_months)),      # representative government's party composition over time
            }
        }

    ######## ######## ######## METHODS ######## ######## ########

    def add_run(self, run: object):
        for stat_key, stat_val in run.f_stat.items():
            for measure_key, measure_val in stat_val.items():
                self.f_stat[stat_key][measure_key] = np.vstack((self.f_stat[stat_key][measure_key], np.array(measure_val)))

        for stat_key, stat_val in run.hh_stat.items():
            for measure_key, measure_val in stat_val.items():
                self.hh_stat[stat_key][measure_key] = np.vstack((self.hh_stat[stat_key][measure_key], np.array(measure_val)))

        if run.sim.gov_exists():
            for stat_key, stat_val in run.g_stat.items():
                for measure_key, measure_val in stat_val.items():
                    if len(measure_val) == 0: continue                  # only add party data for the representative government
                    self.g_stat[stat_key][measure_key] = np.vstack((self.g_stat[stat_key][measure_key], np.array(measure_val)))
        
    def plot_money(self):
        x = range(np.size(self.f_stat['sum']['money'], axis=1))
        y = np.mean(self.f_stat['sum']['money'], axis=0)
        e = stats.sem(self.f_stat['sum']['money'])

        fig, ax = plt.subplots()
        plt.errorbar(x, y, e)

        ax.set(xlabel='Months', ylabel='Money', title='Money')
        ax.grid()
        ax.legend()
        plt.show()

    def invoke_plots(self):
        self.plot_money()