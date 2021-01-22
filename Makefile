# Author: Alessandro De Piccoli
# Makefile for the project Shanatomy
# If you know what you are doing, just edit...

SHELL := /bin/bash
.DEFAULT_GOAL := base-test

#===============================================================================
# Mandatory variables

PYTHON = /usr/bin/python3

#===============================================================================

base-test: setup
	@echo "Building essentials for SHA-1 32 bits..."
	@echo -e "\t1. Creating models..."
	@$(PYTHON) models_creator.py 32 1 30
	@echo -e "\t2. Creating SHA-1 full system..."
	@$(PYTHON) sha_1_generator.py 32 5 80
	@echo -e "\t3. Creating map of the states of the default string \
	'Chiara'...\n"
	@$(PYTHON) map_designer.py 32 0 Chiara 000
	@echo "Getting last line of the file maps/states_000.txt, i.e., SHA-1 \
	digest..."
	@echo -ne "       = "
	@sed -ne 82p maps/states_000.txt
	@echo "Checking with openssl SHA-1..."
	@echo -n "Chiara" | openssl dgst -sha1
	@echo "Base test done."
	@echo -e "\nWhen you're ready, type <make finalize>.\n"

clean:
	@echo "Saving name_list.txt for serial test..."
	@mv testing/name_list.txt .
	@echo "Saving get_mean.py..."
	@mv testing/get_mean.py .
	@echo "Saving bash scripts..."
	@mv testing/*.sh .
	@echo "Saving sha_1_gf2.txt..."
	@mv structures/gf2/sha_1_gf2.txt .
	@echo "Cleaning..."
	@rm -rf __pycache__ maps models structures temp testing
	@echo "Restoring testing directory..."
	@mkdir testing
	@mv name_list.txt get_mean.py *.sh testing
	@echo "Done."

finalize:
	@echo "Simplifications..."
	@echo -n "The digest of 'Chiara' to check the simplification: "
	@$(PYTHON) sha_1_simplifier.py 32
	@echo "Translation to CNF... (this could take a while)"
	@$(PYTHON) sha_1_translator.py 1 structures/sha_1_first_block.txt
	@echo -e "\nYou're now ready to enjoy Shanatomy. :-)"

setup:
	@echo -e "\nMaking directories..."
	@mkdir maps
	@mkdir models
	@mkdir models/cnf
	@mkdir models/equations
	@mkdir structures
	@mkdir structures/gf2
	@mkdir temp
	@echo "Moving sha_1_gf2.txt in structures/gf2"
	@mv sha_1_gf2.txt structures/gf2
	@echo -e "Setup done.\n"

