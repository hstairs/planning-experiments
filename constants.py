NAME = "NAME"
PATH_TO_DOMAINS = "PATH_TO_DOMAINS"
PATH_TO_RESULTS = "PATH_TO_RESULTS"
PLANNERS_X_DOMAINS = "PLANNERS_X_DOMAINS"
COMPILER = "COMPILER"
DOMAINS = "DOMAINS"
MEMORY = "MEMORY"
TIME = "TIME"
PRIORITY = "PRIORITY"
PPN = "PPN"
CONFIGS = "CONFIGS"

RUNS = "RUNS"
DOMAIN_INSTANCES_ERROR = "ERROR! domain files and problem files don't match in number"

PLANNER_EXE_DOMAIN = "#DOMAIN#"
PLANNER_EXE_INSTANCE = "#INSTANCE#"
PLANNER_EXE_SOLUTION = "#SOLUTION#"

RM_CMD = 'rm -r {}'

SHELL_TEMPLATE = '''
#!/bin/bash
var=$PWD
ulimit -v #MEMORY#

mkdir ~/#PLANNER-DESTINATION#
cp -r ~/#PLANNER-SOURCE#/* ~/#PLANNER-DESTINATION#

#cd ~/#PLANNER-DESTINATION#
cd ~/#PLAN-LOCALIZATION#

'''