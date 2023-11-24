# -*- coding: utf-8 -*-
"""
    Created by: Andrés Segura-Tinoco
    Version: 0.2
    Created on: Nov 24, 2023
    Updated on: Nov 24, 2023
    Description: Run all ETL processes.
"""

import generate_argument_data as gad
import generate_network_data as gnd
import generate_proposal_data as gpd
import generate_word_cloud as gwc


def main():
    gad.main()
    gnd.main()
    gpd.main()
    gwc.main()


#####################
### START PROGRAM ###
#####################
if __name__ == "__main__":
    main()
#####################
#### END PROGRAM ####
#####################
