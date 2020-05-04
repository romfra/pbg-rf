# -*- coding: utf-8 -*-
"""
Created on Sat May  2 11:27:55 2020

@author: Romina
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 18:54:19 2020

@author: Romina
"""
import math
from functools import reduce

class Calculator(object):
    
    def get_num1(self):
        num1 = input('Enter the first list of numbers separated by space: ')
        num1_list = num1.split()
        return num1_list
    
    def get_num2(self):
        num2 = input('Enter the second list of numbers separated by space: ')
        num2_list = num2.split()
        return num2_list
    
    def check_list(self, num1, num2):
        # if the list have different number of values the alert will be displayed. 
        # The calculation will be executed for the first same number of values
        if len(num1) != len(num2):
            answ = input('The lists have a different number of elements.'+ 
                         '\nThe operation will be executed for the first same number of values. '+
                         '\nPress the enter Key to calculate')
            return answ
    
    def gen_sum(self,num1):
        calc = 0
        for n1 in num1:
            calc = calc + int(n1)
            yield(calc)
    
# define function for addition operation     
    def add(self, num1, num2):
        if len(num2) > 0:
            # sum of each element in the lists. List comprehension syntax
            return [(int(n1) + int(n2)) for n1, n2 in zip(num1, num2)]
        else:
            # using the geneerator created in the gen_sum to add each single value of the list
            return self.gen_sum(num1)
        
#define function for subtraction operation
    def subtract(self,num1, num2):
        if len(num2) > 0:
            return list(map(lambda n1, n2: int(n1) - int(n2), num1, num2))            
        else:
            # calculate the running difference
            return reduce(lambda n1, n2 : int(n1) - int(n2), num1)        

#define function for division operation
    def divide(self,num1, num2):
        # Filter out the values = 0 in the second list because denominator has to be <> 0
        return list(map(lambda n1,n2: int(n1)/int(n2), num1, filter(lambda n2: int(n2) != 0, num2)))
            
            
# define function for moltiplication operation between lists
    def multiply(self, num1, num2):
        return list(map(lambda n1,n2: int(n1) * int(n2), num1, num2))

# define function for square root operation
    def square_root(self,num1):   
        # if in the generator negative numbers are inserted, they are filtered out
        # generator comprehension syntax
        return (int(n1)**0.5 for n1 in num1 if int(n1) > 0)  
        
          
# define function for power operation
    def power(self,num1,num2):
        return list(map(lambda n1,n2: pow(int(n1),int(n2)), num1, num2))
        
# define function for logarithm operation  
    def log(self,num1,num2, logarithm_opt):
       
        if logarithm_opt in ['2', 'log']:
            # user has chosen to calculate the logarithm with defined base      
            # if in the num1_list negative numbers are inserted they are filtered out
            return list(map(lambda n1, n2: round(math.log(int(n1), int(n2)),2), filter(lambda n1: int(n1) > 0, num1) , num2))
        elif logarithm_opt in ['1', 'ln']:
             num2 = ''
             return list(map(lambda n1: round(math.log(int(n1)),2), filter(lambda n1: int(n1) > 0, num1)))
        else:
        #user has typed one option of logarithm not available
            print('You typed a choice not valid')

# define function for sine operation
    def sen(self,num1):
        return list(map(lambda n1: math.sin(math.radians(int(n1))) , num1))

#define function for cosine operation
    def cos(self,num1):
        return list(map(lambda n1: math.cos(math.radians(int(n1))), num1))
        
#define function for tangent operation
    def tan(self,num1):
        # generator comprehension to calculate the tan of each value in the list
        return (math.tan(math.radians(int(n1))) for n1 in num1)

    
    def process_calculation(self):
        op_choice = input('1 Mathematical operations \n2 Trigonometric operations \nChoose one of these two types of operations: ')
        
        if op_choice == '1':
            
            operator = input('1 or + to calculate addition \n2 or - to calculate subtraction \n3 or / to calculate division'+
                             '\n4 or * to calculate multiplication \n5 or sqr to calculate square root \n6 or ^ to calculate power'+
                             '\n7 to calculate logarithm \nEnter the operator (see options above): ')
            
            num1_list = self.get_num1()
                       
            if operator in ['1', '+']:
                # addition operation chosen
                answer = input('Would you like calculate the running total of values inserted? y/n ')
                if answer == 'y':
                    # running total calculation chosen
                    running_total = self.add(num1_list,'')
                    for value in running_total:
                        #print each single element of the generator
                        print('Sum to the next value = ', value) 
                else:
                    num2_list = self.get_num2()
                    self.check_list(num1_list, num2_list)
                    calc = self.add(num1_list, num2_list)
                    result = 'The sum of {0} and {1} is = '
                    print(result.format(num1_list,num2_list), calc)
                    
            elif operator in ['2', '-']:
                # subtraction operation chosen
                answer = input('Would you like calculate the running difference of values inserted? y/n ')
                if answer == 'y':
                    # running difference calculation chosen
                    calc = self.subtract(num1_list, '')
                    result = 'Running difference of the values {0} is = '  
                    print(result.format(num1_list), calc)
                else:
                    num2_list = self.get_num2()
                    self.check_list(num1_list, num2_list)
                    calc = self.subtract(num1_list, num2_list)
                    result = 'The difference between {0} and {1} is = '
                    print(result.format(num1_list, num2_list), calc)
            
            elif operator in ['3', '/']:
                # division operation chosen
                num2_list = self.get_num2()
                self.check_list(num1_list, num2_list)
                calc = self.divide(num1_list, num2_list)
                result = 'The possible division (values divided by 0 are excluded) between sequence {0} and sequence {1} is = '
                print(result.format(num1_list,num2_list), calc)
                
            elif operator in ['4', '*']:
                # multiplication operation chosen
                num2_list = self.get_num2()
                self.check_list(num1_list, num2_list)
                calc = self.multiply(num1_list, num2_list)
                result = '{0} multiplied by {1} is = '
                print(result.format(num1_list,num2_list), calc)
                
            elif operator in ['5' , 'sqr']:
                # square root for list values chosen
                calc = self.square_root(num1_list)
                for value in calc:
                    print('The square root of the positive value inserted is = ', value)  
                    
            elif operator in ['6','^']:
                # power operation chosen
                num2_list = self.get_num2()
                self.check_list(num1_list, num2_list)
                calc = self.power(num1_list, num2_list)
                result = 'The value of {0}power{1} is = '
                print(result.format(num1_list,num2_list),calc)
                    
            elif operator in ['7']:
                # logarithm operation chosen
                logarithm_opt = input('1 or ln to calculate the natural logarithm for the sequence'+
                              '\n2 or log to calculate the logarithm of specified base'+
                              '\nWhich type of logarithm you want to calculate? ')
                
                if logarithm_opt  in ['1', 'ln']:
                    # natural logarithm calculation
                    calc = self.log(num1_list, '',logarithm_opt)
                    print('Natural logarithm of the positive numbers in the sequence {0}'.format(num1_list), 'is = ', calc)
                else:
                    # logarithm with specified base chosen
                    # the base inserted as float has to be transformed in a list with as many repeated elements
                    # as the lenght of list with values to calculate the log. The negative values are 
                    # filteres out from the first list inserted
                    num1_list_new = list(filter(lambda n1: int(n1) > 0, num1_list))
                    num2 = float(input('Enter the base of logarithm: '))
                    num2_list = [num2] * len(num1_list_new)
                    calc = self.log(num1_list_new, num2_list, logarithm_opt)
                    result = 'The logarithm base {0} of positive numbers in the sequence {1} is = '
                    print(result.format(num2_list[0],num1_list),calc)

        
        elif op_choice == '2':
            # user has chosen to compute a trigonometric function
            operator = input('1 or sin to calculate sin of the angle \n2 or cos to calculate cosin of the angle'+
                             '\n3 or tan to calculate tangent of the angle \nEnter the trigonometric operator: ')            

            angle = input('Enter the angle values list: ')
            angle_list = angle.split()
            
            if operator in ['1', 'sin']:   
                calc = self.sen(angle_list)
                print('The sin of values list in degree is = ', calc)
            elif operator in ['2', 'cos']:
                calc = self.cos(angle_list)
                print('The cosin of values list in degree is = ', calc)
            elif operator in ['3', 'tan']:
                calc = self.tan(angle_list)  
                for value in calc:
                    print('The tangent of the value inserted in degree is = ', value)
            else:
                # user has typed an option not available in the trigonometric functions menu
                print('You typed a trigonometric function option not available.')
        else:
        # user has typed an option not available in the function menu
            print('You typed a number option not available.')
                    

if __name__ == '__main__':
    calculator = Calculator()
    proceed = 'y'
    while proceed == 'y':
        calculator.process_calculation()
        proceed = input('Would you like to continue? y/n ')
