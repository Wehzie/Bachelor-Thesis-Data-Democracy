

# Lengnick, M. (2013). Agent-based macroeconomics: A baseline model. Journal of Economic Behavior and Organization, 86, 102-120. doi:10.1016/j.jebo.2012.12.021

from simulation import Simulation
from super_stat import Super_stat

def main():
    num_months = 15
    gov_types = [None, 'data', 'rep', 'dir']
    gov_type = gov_types[0]                             # BUG: 0/None doesn't work on second run
    runs = 2
    plot_per_run = False if runs > 1 else True        # show and save plots for a single run only when doing one run in total

    super_stat = Super_stat(num_months)
    for run in range(runs):
        sim = Simulation(num_months, gov_type, plot_per_run)
        sim.print_sim_step(f"RUN {run}")
        sim.start_sim()
        if runs > 1: super_stat.add_run(sim.stat)
    if runs > 1: super_stat.invoke_plots()

if __name__ == "__main__":
    main()
    
