

# Lengnick, M. (2013). Agent-based macroeconomics: A baseline model. Journal of Economic Behavior and Organization, 86, 102-120. doi:10.1016/j.jebo.2012.12.021

from simulation import Simulation
from super_stat import Super_stat

def main():
    num_months = 20
    gov_types = [None, 'data', 'rep', 'dir']
    gov_type = gov_types[3]
    runs = 2

    #print("(1) Default parameters.")
    #print("(2) Set number of months."

    #user_input = int(input())
    #if(user_input == 2): num_months = int(input("Enter number of months: ")) 
    
    super_stat = Super_stat(num_months)
    for run in range(runs):
        sim = Simulation(num_months, gov_type)  # TODO: in multiple runs no plots should pop up
        sim.print_sim_step(f"RUN {run}")
        sim.start_sim()
        super_stat.add_run(sim.stat)
    super_stat.invoke_plots()

if __name__ == "__main__":
    main()
    
