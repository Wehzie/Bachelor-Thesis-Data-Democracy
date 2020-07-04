

######## ######## ######## IMPORTS ######## ######## ########

from simulation import Simulation
from stat_runs import Stat_runs

######## ######## ######## MAIN ######## ######## ########

def main():
    '''
    This program models an economy, see the README for further details.

    This method controls duration and repetitions of the simualtion.
    Additionally it controls what government agent to instantiate.
    Further paramaters of the simulation are to be modified in Simulation class.
    '''

    num_months = 10
    gov_types = ['none', 'data', 'rep', 'dir']
    gov_type = gov_types[2]
    runs = 2
    plot_per_run = False if runs > 1 else True        # show and save plots for a single run only when doing one run in total

    stat_runs = Stat_runs(num_months, gov_type, runs)   # TODO: call with sim
    for run in range(runs):
        sim = Simulation(num_months, gov_type, plot_per_run, runs)
        sim.print_sim_step(f"RUN {run}")
        sim.start_sim()
        if runs > 1: 
            stat_runs.set_sim(sim)
            stat_runs.add_run(sim.stat)
    if runs > 1: stat_runs.invoke_plots()

if __name__ == "__main__":
    main()
    
