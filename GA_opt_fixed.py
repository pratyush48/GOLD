'''This code is written by @Pratyush Nandi-Research Assistant at IIIT Bangalore
   Functionality of this code is to implement a genetic algorithm, which takes in positions of Hblocks(Memory and DSP) as input parameters
   and generates the best position of such blocks which when implemented on VTR gives you the best configuration of FPGA for that particular application
   interms of AREA x DELAY'''
from cmath import nan
import numpy  as np
import random as rnd
import gen_script 
# think about how to keep priotities in one array
# decision_vars_blocks = [10]-->[priority of clb]
# decision_vars_mat_m = [[20,1,2],[20,1,2],[20,1,2],[20,1,2],[20,1,2],[20,1,2],[20,1,2],[20,1,2]]--->[startx, starty, priority]{8 such blocks}
# decision_vars_mat_dsp = [[20,1,2],[20,1,2],[20,1,2],[20,1,2],[20,1,2],[20,1,2]]--->[startx, starty, priority]{5 such blocks}
# num_individuals = 10
# num_generation = 200
# crossver_prob = 0.87
# mutation_prob = 0.7

class gen_alg():
    def __init__(self,dev_var, num_ind, num_gen, cross_prob, mut_prob):
        print("reached genetic algorithm")
        self.dev_var = dev_var
        self.num_ind = num_ind
        self.num_gen = num_gen
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob
        self.monitor = 1
        self.max = 0
    
    def __del__(self):
        print("delted object of class gen_alg")

    #Fitness functions gets the area x delay product for a particular solution
    def fitness_function(self,sol):
        gen_object = gen_script.gen(sol,self.monitor)
        print("back to ga script")
        [fit_value,monitor] = gen_object.main()
        self.monitor = monitor
        del gen_object
        if(fit_value > self.max): 
            self.max = fit_value
            self.max = self.max*10000
        if(fit_value == 1):
            fit_value = self.max
        return fit_value
    
    def initiate(self):
        population_bag = []
        for i in range(self.num_ind):
            rnd_sol = self.dev_var.copy()
            population_bag.append(rnd_sol)
        #array of population bags of solution-->[10,[[12,2,3]....],[[1,2,3]......]]
        return np.array(population_bag)

    #Creates dictionary for solutions from a particular population/generation
    def eval_fit_pop(self,population_bag):
        res = {}
        fit_val_list = []
        sols = []
        for sol in population_bag:
            fit_val_list.append(self.fitness_function(sol))
            sols.append(sol)

        res["fit_val"] = fit_val_list
        min_wgt = [np.max(list(res["fit_val"]))-i for i in list(res["fit_val"])] #normalizing it?
        if(sum(min_wgt) == 0):
            res["fit_wgt"] = [i/self.max for i in min_wgt]
        else:
            res["fit_wgt"] = [i/sum(min_wgt) for i in min_wgt]
        res["sol"] = np.array(sols)
        #dictionary of solution-->{ fit_val: 
        #                           fit_wgt: 
        #                           sol:[[10],[[12,2,3]....],[[1,2,3]......]],..]}
        return res
    
    def pick(self,population_bag,fit_bag_evals):
        #array of dictionaries
        # self.monitor = self.monitor-1
        # fit_bag_evals = self.eval_fit_pop(population_bag)
        t = True
        while t:
            rnIndex = rnd.randint(0, len(population_bag)-1)
            rnPick = fit_bag_evals["fit_wgt"][rnIndex]
            r = rnd.random()
            if r <= rnPick:
                pickedSol = fit_bag_evals["sol"][rnIndex]
                t = False
        #array of solution [10,[[12,2,3]....],[[1,2,3]......]]
        return pickedSol

    def crossover(self, solA, solB):
        #solA and solB are array of solutions---->[10,[[12,2,3]....],[[1,2,3]......]]
        # offspring = [10,[[np.nan,np.nan,np.nan],[np.nan,np.nan,np.nan],[np.nan,np.nan,np.nan],[np.nan,np.nan,np.nan],[np.nan,np.nan,np.nan],[np.nan,np.nan,np.nan],[np.nan,np.nan,np.nan],[np.nan,np.nan,np.nan]],[[np.nan,np.nan,np.nan],[np.nan,np.nan,np.nan],[np.nan,np.nan,np.nan],[np.nan,np.nan,np.nan],[np.nan,np.nan,np.nan]]]
        offspring = solA
        #len(solA) = 3
        n = len(solA)  #---> 3   
        #offspring[k] = [np.nan for i in range(n)]
        num_els = np.ceil(n*(rnd.randint(10,90)/100)) #??
        str_pnt = rnd.randint(0,n-2)
        end_pnt = n if int(str_pnt+num_els) > n else int(str_pnt+num_els)
        blockA = list(solA[str_pnt:end_pnt])
        offspring[str_pnt:end_pnt] = blockA
        for i in range(1,n):
            if list(blockA).count(solB[i]) == 0:
                for j in range(1,n):
                    # print(offspring)
                    if (offspring[j][0][0] == solA[j][0][0]):
                        if(len(offspring[j]) == len(solB[i])):    
                            offspring[j] = solB[i]
                            break
        # print("Last stage before crossover")
        # print(offspring)
        return offspring
    
    def swap(self,sol, pos_1, pos_2):
        #sol is array of solutions of 1 kind
        result = sol.copy()
        el_1 = sol[pos_1]
        el_2 = sol[pos_2]
        result[pos_1] = el_2
        result[pos_2] = el_1
        return result 

    def mutation(self,sol):
        #array of solution [10,[[12,2,3]....],[[1,2,3]......]]
        n = len(sol) #-->3
        x = []
        y = []
        z = 0
        for i in range(n):
            if(i == 0):
                if(rnd.random() <= self.mut_prob):
                    sol[i] = rnd.randint(1,10)
            else:
                for j in range(len(sol[i])):
                    for k in range(len(sol[i][j])):
                        if(rnd.random() <= self.mut_prob):
                            if(k == 0):
                                num = rnd.randint(3,20)
                                while x.count(num):
                                    num = rnd.randint(3,20)
                                sol[i][j][k] = num
                                x.append(sol[i][j][k])
                            elif(k == 1):
                                num = rnd.randint(3,20)
                                while y.count(num):
                                    num = rnd.randint(3,20)
                                sol[i][j][k] = num
                                y.append(sol[i][j][k])
        result = sol
        return result

    def func_m1(self):
        #array of population bags 
        pop_bag = self.initiate()
        g = 0
        t_con = [0 for i in range(0,self.num_gen)]
        for gen in range(self.num_gen):
            #array of dictionaries of results
            #called this function for first time--->self.monitor inc
            pop_bag_fit = self.eval_fit_pop(pop_bag)
            #final solution would be in the form--->-->[10,[[12,2,3]....],[[1,2,3]......]]
            best_fit = np.min(pop_bag_fit["fit_val"])
            best_fit_index = pop_bag_fit["fit_val"].index(best_fit)
            best_sol = pop_bag_fit["sol"][best_fit_index]

            if gen == 0:
                #clb
                best_fit_global = best_fit
                best_sol_global = best_sol
            else:
                if best_fit <= best_fit_global:
                    best_fit_global = best_fit
                    best_sol_global = best_sol
            
            new_pop_bag = []

            for i in range(self.num_ind):
                pA = self.pick(pop_bag,pop_bag_fit)
                pB = self.pick(pop_bag,pop_bag_fit)
                new_element = pA

                if rnd.random() <= self.cross_prob:
                    new_element = self.crossover(pA,pB)

                if rnd.random() <= self.mut_prob:
                    new_element = self.mutation(new_element)

                new_pop_bag.append(new_element)

            pop_bag = np.array(new_pop_bag)

            print(f"Best fitness: {best_fit_global}")
            print(f"Best solution: {best_sol_global}")
            print("Generation number:"+str(gen))
            filename = "output.txt"
            with open(filename, mode="a+", encoding="utf-8") as message:
                message.write(f"Best fitness: {best_fit_global}")
                message.write(f"Best solution: {best_sol_global}")
                print(f"... wrote {filename}")
            t_con[g] = best_fit_global
            check = 0
            if(g >= 14):
                for i in range(g-14,g+1):
                    if(t_con[i] == t_con[g]):
                        check = check+1
                    if(check >= 14):
                        print("breaking condition reached....")
                        return best_fit_global
            g = g+1