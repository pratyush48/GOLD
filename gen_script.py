'''This code is written by @Pratyush Nandi-Research Assistant at IIIT Bangalore
   Functionality of this code is to generate arch file based on solution prvided by Genetic algorithm'''
from logging import error
import jinja2
from jinja2 import Environment, FileSystemLoader
import os
import extraction_script
 
class gen():
    def __init__(self,sol,monitor):
        print("reached genration script")
        self.clb_priority = sol[0] 
        self.dsps = sol[1]
        self.mems = sol[2]
        self.environment = Environment(loader=FileSystemLoader("templates/"))
        self.template = self.environment.get_template("k6_frac_N10_frac_chain_depop50_mem32K_40nm.xml")
        self.monitor = monitor

    def __del__(self):
        print("deleted gen script object")

    def main(self):
        filename = "my_arch.xml"
        content = self.template.render(
            clb_priority=self.clb_priority,
            dsps=self.dsps,
            mems=self.mems
        )
        with open('vtr-verilog-to-routing/vtr_flow/arch/timing/'+filename, mode="w", encoding="utf-8") as message:
            message.write(content)
            print(f"... wrote {filename}")
        #run the vtr-flow
        status = os.system('vtr-verilog-to-routing/vtr_flow/scripts/run_vtr_task.py regression_tests/vtr_reg_basic/basic_timing')
        print("ran vtr-flow--sucessfully")
        #extraction script
        if(status == 0):
            if(self.monitor < 10):
                print("reading from run00"+str(self.monitor))
                ext_object = extraction_script.extract("vtr-verilog-to-routing/vtr_flow/tasks/regression_tests/vtr_reg_basic/basic_timing/run00"+str(self.monitor)+"/parse_results.txt") #-->add file name
            elif(self.monitor >= 10 and self.monitor < 100):
                print("reading from run0"+str(self.monitor))
                ext_object = extraction_script.extract("vtr-verilog-to-routing/vtr_flow/tasks/regression_tests/vtr_reg_basic/basic_timing/run0"+str(self.monitor)+"/parse_results.txt") #-->add file name
            else:
                print("reading from run"+str(self.monitor))
                ext_object = extraction_script.extract("vtr-verilog-to-routing/vtr_flow/tasks/regression_tests/vtr_reg_basic/basic_timing/run"+str(self.monitor)+"/parse_results.txt") #-->add file name
            ad_prod = ext_object.main()
            print("test-no.:"+str(self.monitor))
            print("area x delay:"+str(ad_prod))
            del ext_object
            return [ad_prod,self.monitor+1]
        else:
            return False
