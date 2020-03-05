

from simulation import start_sim


def main():
    num_months = 2000

    print("(1) Default parameters.")
    print("(2) Set number of months.")

    user_input = int(input())
    if(user_input == 2): num_months = int(input("Enter number of months: ")) 

    start_sim(num_months)

if __name__ == "__main__":
    main()
    