

######## ######## ######## IMPORTS ######## ######## ########

from simulation import Simulation
from stat_super import Stat_super

######## ######## ######## MAIN ######## ######## ########

def main():
    '''
    This program models an economy, see the README for further details.

    This method controls duration and repetitions of the simualtion.
    Additionally it controls what government agent to instantiate.
    Further paramaters of the simulation are to be modified in Simulation class.
    '''

    num_months = 50
    gov_types = [None, 'data', 'rep', 'dir']
    gov_type = gov_types[2]
    runs = 2
    plot_per_run = False if runs > 1 else True        # show and save plots for a single run only when doing one run in total

    stat_super = Stat_super(num_months)
    for run in range(runs):
        sim = Simulation(num_months, gov_type, plot_per_run)
        sim.print_sim_step(f"RUN {run}")
        sim.start_sim()
        if runs > 1: stat_super.add_run(sim.stat)
    if runs > 1: stat_super.invoke_plots()

if __name__ == "__main__":
    main()
    
