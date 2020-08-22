

######## ######## ######## IMPORTS ######## ######## ########

from simulation import Simulation
from stat_runs import Stat_runs
import sys
import argparse
import random
from pathlib import Path

######## ######## ######## MAIN ######## ######## ########

def main():
    '''
    This program models an economy to test whether financial equality can be regulated by a flat rate tax and universal basic income.

    This main method controls duration and repetitions of the simulation.
    It also sets the number of firms and households simulated.
    Additionally it controls what government agent to instantiate and how data is plotted.
    The above parameters are controlled here since they determine the computational complexity of the program.
    Further paramaters of the simulation are to be modified in the Simulation class.
    
    See the README for further details.
    '''

    # random seed for reproducibility
    random.seed(15532)

    # command line control of initial parameters
    parser = argparse.ArgumentParser(description='Set initial running parameters for the simulated economy.')
    parser.add_argument("--months", type=int, nargs='?', default=100, help="set the number of months simulated per run")
    parser.add_argument("--runs", type=int, nargs='?', default=1, help="set number of runs to simulate")
    parser.add_argument("--gov", type=str, nargs='?', choices=['none', 'rep', 'dir'], default='none', help="select government implementation")
    parser.add_argument("--f", type=int, nargs='?', default=100, help="number of firms used in a simulation")
    parser.add_argument("--hh", type=int, nargs='?', default=1000, help="number of households used in a simulation")
    args = parser.parse_args()
    num_months = args.months
    runs = args.runs
    gov_type = args.gov
    num_f = args.f
    num_hh = args.hh

    # print initial conditions and write them to file
    print_hashes = "######## ######## ########"
    initial_conditions = f"""
{print_hashes:<30} INITIAL CONDITIONS {print_hashes:>58}\n
{print_hashes:<30} {'MONTHS:':>15} {num_months:>10}
{print_hashes:<30} {'RUNS:':>15} {runs:>10}
{print_hashes:<30} {'GOVERNMENT:':>15} {gov_type:>10}
{print_hashes:<30} {'FIRMS:':>15} {num_f:>10}
{print_hashes:<30} {'HOUSEHOLDS:':>15} {num_hh:>10}"""
    print(initial_conditions)
    Path("./img").mkdir(parents=True, exist_ok=True)     # make sure /img/ directory exists for writing plots and initial conditions
    with open("img/fig_" + gov_type + "_initial_conditions.txt", "w") as f: 
        f.write(initial_conditions)

    # parameters for plotting
    plot_param = {
        'plot_per_run': False if runs > 1 else True,    # show and save plots for a single run only when doing one run in total
        'save_pgf': False,                               # save plots as Progressive Graphics File for LaTeX
        'save_pdf': False,                               # save plots as Portable Document Format
        'save_png': True,                               # save plots as Portable Network Graphics at 300 DPI
    }

    # run the simulation for a set number of runs then exit the program
    stat_runs = Stat_runs(num_months, runs, gov_type, num_f, num_hh, plot_param)  
    for run in range(runs):
        sim = Simulation(num_months, runs, gov_type, num_f, num_hh, plot_param)
        print(f"\n{print_hashes:<30} {'RUN:':>15} {run:>10} {print_hashes:>50}\n")
        sim.start_sim()
        if runs > 1:
            stat_runs.set_sim(sim)
            stat_runs.add_run(sim.stat)
    if runs > 1:
        print(f"\n{print_hashes:<30} {'CREATING PLOTS':>15}")
        stat_runs.invoke_plots()
    print(f"\n{print_hashes:<30} {'EXITING PROGRAM':>15} {print_hashes:>61}")

if __name__ == "__main__":
    main()
    
