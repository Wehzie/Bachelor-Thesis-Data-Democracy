

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

    # parameters in the block below are computationally most relevant
    num_months = 5                                     # number of months simulated per run
    runs = 2                                            # set number of runs to simulate
    gov_types = ['none', 'data', 'rep', 'dir']          # four forms of government are implemented
    gov_type = gov_types[0]                             # select between implementations of a government
    num_f = 100                                         # number of forms used in a simulation
    num_hh = 1000                                       # number of households used in a simualtion

    # parameters for plotting
    plot_param = {
        'show_plots': True,                             # set whether plots are showed or just saved 
        'plot_per_run': False if runs > 1 else True,    # show and save plots for a single run only when doing one run in total
        'save_pgf': True,                               # save plots as Progressive Graphics File for LaTeX
        'save_pdf': True,                               # save plots as Portable Document Format
        'save_png': True,                               # save plots as Portable Network Graphics at 300 DPI
    }

    # run the simulation for a set number of runs
    stat_runs = Stat_runs(num_months, runs, gov_type, num_f, num_hh, plot_param)  
    for run in range(runs):
        sim = Simulation(num_months, runs, gov_type, num_f, num_hh, plot_param)
        sim.print_sim_step(f"RUN {run}")
        sim.start_sim()
        if runs > 1:
            stat_runs.set_sim(sim)
            stat_runs.add_run(sim.stat)
    if runs > 1: stat_runs.invoke_plots()

if __name__ == "__main__":
    main()
    
