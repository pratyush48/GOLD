'''This code is written by @Pratyush Nandi-Research Assistant at IIIT Bangalore
   Functionality of this code is to implement the main script or the one which initiates everything'''
import gen_script
import GA_opt_fixed
import extraction_script
 
# initial_sol = [10,[[5,4,20],[7,4,20],[5,8,20],[7,8,20],[5,12,20],[7,12,20],[5,16,20],[7,16,20]],[[17,4,20],[19,4,20],[17,12,20],[19,12,20],[17,20,20]]]
initial_sol = [10,[[6,1,20], [8,1,20], [9,1,20], [10,1,20], [11,1,20], [12,1,20], [13,1,20], [14,1,20]],[[2, 1, 20], [3, 1, 20], [4, 1, 20], [5, 1, 20], [6, 1, 20]]]
num_ind = 5
num_gen = 50
cross_prob = 0.87
mut_prob = 0.7
ga_object = GA_opt_fixed.gen_alg(initial_sol,num_ind,num_gen,cross_prob,mut_prob)
fit_value = ga_object.func_m1()
del ga_object
