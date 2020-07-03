

from simulation import Simulation
from statistician import Statistician
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

        if run.sim.gov_exists():
            for stat_key, stat_val in run.g_stat.items():
                for measure_key, measure_val in stat_val.items():
                    if len(measure_val) == 0: continue                  # only add party data for the representative government
                    self.g_stat[stat_key][measure_key] = np.vstack((self.g_stat[stat_key][measure_key], np.array(measure_val)))
        
    def plot_money_old(self):
        x = range(np.size(self.f_stat['avg']['money'], axis=1))
        y1_f_money = np.mean(self.f_stat['avg']['money'], axis=0)
        y2_hh_money = np.mean(self.hh_stat['avg']['money'], axis=0)
        e1 = stats.sem(self.f_stat['avg']['money'])
        e2 = stats.sem(self.hh_stat['avg']['money'])

        fig, ax = plt.subplots()
        plt.errorbar(x, y1_f_money, e1, color='r', label='Money firm average')
        plt.errorbar(x, y2_hh_money, e2, color='b', label='Money household average')

        ax.set(xlabel='Months', ylabel='Money', title='Money distribution between firms and households')
        ax.grid()
        ax.legend()
        fig.savefig('fig_'+ self.gov_type +'_money_old.png')
        plt.show()

    def invoke_plots(self):
        #self.plot_money()
        self.plot_money_old()