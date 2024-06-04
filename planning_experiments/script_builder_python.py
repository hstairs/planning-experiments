from os import path
from planning_experiments.data_structures.environment import Environment, System
import pkg_resources

class ScriptBuilder:

    # BASH = "#!/bin/bash"
    # PWD = "var=$PWD"

    def __init__(self, env: Environment,
                       system: System,
                       domain_name: str,
                       instance_name: str,
                       results: str,
                       system_dst: str,
                       time: int,
                       system_exe: str,
                       stdo: str,
                       stde: str,
                       script_name: str,
                       info_dict_path: str,
                       script_folder: str,
                       memory: int = None) -> None:
        
        self.system = system
        self.enviorment = env
        self.inner_script = []
        self.outer_script = []
        self.memory = memory
        self.system_dst = system_dst
        self.time = time
        self.system_exe = system_exe
        self.stdo = stdo
        self.stde = stde
        self.script_name = script_name
        self.script_folder = script_folder
        self.info_dict_path = info_dict_path
        self.domain_name = domain_name
        self.instance_name = instance_name
        self.results = results

    def get_script(self):

        self.outer_script.append(f'import os')
        self.outer_script.append(f'import shutil')
        self.outer_script.append(f'os.makedirs("{self.system_dst}")')

        self.manage_dependencies()
        self.outer_script.append(f'os.chdir("{self.system_dst}")')

        exec_cmd = f'os.system("python {path.join(self.script_folder, self.script_name)} 2>> {self.stde} 1>> {self.stdo}")'

        if self.time != "None":
            exec_cmd = f'os.system("/usr/bin/time -f \'Total Runtime: %e\' timeout --signal=HUP {self.time} python {path.join(self.script_folder, self.script_name)} 2>> {self.stde} 1>> {self.stdo}")'

        self.outer_script.append(exec_cmd)
       
        ## INNER SCRIPT ##
        self.inner_script.append(f'import os')
        exe_list = self.manage_complex_cmd()
        
        if self.memory != 'None':
            self.inner_script.append(f'os.system("ulimit -Sv {self.memory}")')

        self.inner_script += exe_list

        
        #################
        # if self.enviorment.delete_systems:
        #     self.outer_script.append(f'rm -r -f {self.system_dst}')
        
        # save_results_path = pkg_resources.resource_filename(__name__, f'./bin/save_results.py')
        # self.outer_script.append(f'python {save_results_path} {self.results} {self.system.name} {self.domain_name} {self.instance_name}')
        
        inner_script_str = '\n'.join(self.inner_script)
        outer_script_str = '\n'.join(self.outer_script)
        return inner_script_str, outer_script_str
    
    def set_memory(self, memory: int):
        self.memory = memory

    def manage_dependencies(self):
        dependencies = set([dep for dep in self.system.get_dependencies()])
        for dep in dependencies:
            self.outer_script.append(f'os.system("cp -r {path.abspath(dep)} {self.system_dst}")')
    
    def manage_complex_cmd(self):
        if isinstance(self.system_exe, list):
            cmd_chain = []
            for cmd in self.system_exe:
                cmd_chain.append(f'os.system("{cmd}")')
            return cmd_chain
        else:
            return [f'os.system("{self.system_exe}")']




"""
#!/bin/bash
var=$PWD
mkdir path-to-dir
cp -r dir-a dir-b
./exe.sh 2>> err.txt 1>> /log.txt
rm -r -f dir-b
"""