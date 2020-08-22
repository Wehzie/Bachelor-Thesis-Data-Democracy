

from simulation import Simulation
from statistician import Statistician
import numpy as np

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

