# Bachelor-Thesis-Data-Democracy

This program models a simple economy.
Two types of relationships exist between firms and households.
Firstly, firms produce items which are sold to households.
Secondly, firms employ households to produce items.
Each month, item prices and wages are updated based on supply and demand.
This is done in a multi-agent systems (MAS) manner.
Here, each agent makes its own decisions with the limited information available to it. 

Additionally, the program implements twp types of governments responsible for redistributing money by means of a flat rate tax and a universal basic income (UBI). Only households are taxed and receive UBI. The governments differ in the process of determining the flat tax and UBI.
First, this simulation is used to compare both governments.
Second, the effectiveness of redistribution is evaluated by comparing the governments to a setting without redistribution.

## Getting Started

To run the program on you local machine see the following instructions.
 
### Prerequisites

A version of Python 3.5 or greater is needed. On Linux run the following to check your version.

        python3 --version   # Ubuntu, Debian
        python --version    # Arch, Fedora

The Python modules Matplotlib, Numpy and SciPy are needed. Lower versions may work but I have used matplotlib 3.2.1, numpy 1.17.3 and scipy 1.5.1. On Linux run the following to confirm that you have the packages installed.

        pip3 list   # Ubuntu, Debian
        pip list    # Arch, Fedora

### Installing

#### Debian/Ubuntu

Python, pip, Matplotlib and Numpy are installed as follows.

        sudo apt install python3 python3-pip
        pip3 install -U matplotlib numpy scipy

To generate plots in pgf format for use in LaTeX, a form of LaTeX must be installed.
The generation of pgf plots is disabled by default, however it can easily be enabled in `main.py`.

        # this installs the needed packages for pgf creation
        sudo apt install texlive texlive-xetex
        # this installs all packages and languages
        sudo apt install texlive-latex-extra 

## Running the simulation

Clone the project using Git or download manually.

        git clone https://github.com/Wehzie/Bachelor-Thesis-Data-Democracy.git

Before starting the program set your working directory to the project folder.

        cd path/to/Bachelor-Thesis-Data-Democracy

To start the program run the following command. The program will run with default parameters.

        python3 src/main.py

To run the simulation with different parameters open the help menu to learn more about what parameters to set.

        python3 src/main.py --help

To run the simulation in the background after closing the terminal use the following command. Parameters such as --help must stand before the ampersand '&' symbol.

        nohup python3 src/main.py &

Additional parameters about plotting behavior and saving data to file are set in `main.py`.

## Acknowledgments

This program is a Python reimplementation and extension based on the works of the following paper.

- Lengnick, M. (2013). Agent-based macroeconomics: A baseline model. Journal of Economic Behavior and Organization, 86, 102-120. doi:10.1016/j.jebo.2012.12.021

The author of the paper wrote a model in Java and kindly made that code available. He also pointed to a project which lead to a rewrite of the model using a simulation building tool that transpiles to JavaScript. The JavaScript model can be found on https://sim4edu.com/sims/20/LengnickBaselineEconomy-1. In doing the Python rewrite, I mainly relied on the JavaScript code, which is licenced as follows.

 - Copyright 2018 Brandenburg University of Technology, Germany
 - The MIT License (MIT)
 - Luis Gustavo Nardin
 - Gerd Wagner

As such, I would like to thank Matthias Lengnick, Gustavo Nardin and Gerd Wagner for their work.

Furthermore I am happy to have been supervised by Professor Davide Grossi at the University of Groningen in the Netherlands. I am thankful for his patience, a great book recommendation and giving me the confidence I needed to finish the project. A special thank you goes to my Papa, Peter Tappe, who helped clear the fog on questions regarding economics and taxation. Nils Kruse deserves credit for sharing his experience in programming and his sense of good science. We had a particularly long discussion on seeding and reproducibility, he helped review the program and when I needed to make a clear decision he lent me focus. Jonas Zimmermann shared his mathematical expertise and experience in Data Science. Ben Schmidt helped proof read the paper developed alongside this program.
Martijn Luinstra helped me answer questions regarding the JavaScript implementation by Nardin and Wagner.
Julian Arndts pointed me to the works of Milton Friedman on the flat tax and UBI proposal; he was also available to discuss the works of Anthony Atkinson on taxation.

In a more indirect way the student association Cover in Groningen helped me develop the idea for this work. Inspired by the course Data Analytics and Communication I got to write a dystopian article about how data could change democracy for the DisCover magazine. This process lead me to approach Professor Grossi with this thesis idea. Last I would like to thank the rest of my family, friends and especially my grandpa. A la orden catipán.

## Author
This program was developed by Rafael Tappe Maestro at University of Groningen.