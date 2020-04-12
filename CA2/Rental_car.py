
from car import Car, ElectricCar, PetrolCar, DieselCar, HybridCar

class Dealership(object):

    def __init__(self):
        #initialize the lists of different type of cars
        self.electric_cars = []
        self.petrol_cars = []
        self.diesel_cars = []
        self.hybrid_cars = []
                  
            
    def create_current_stock(self, typecar, start):
        #set up the initial stock for each type of cars
        # it has been called in the main (row 100)
        if typecar == 'E':
            for i in range(start):
                self.electric_cars.append(ElectricCar())
        elif typecar == 'P':
            for i in range(start):
               self.petrol_cars.append(PetrolCar())
        elif typecar == 'D':
            for i in range(start):
                self.diesel_cars.append(DieselCar())
        elif typecar == 'H':
            for i in range(start):
                self.hybrid_cars.append(HybridCar())

    def stock_count(self):
        # each list of cars contains Car objects. The len of the list give us the number of cars
        print('Petrol cars in stock: ' + str(len(self.petrol_cars)))
        print('Electric cars in stock: ' + str(len(self.electric_cars)))
        print('Diesel Cars in stock: ' + str(len(self.diesel_cars)))
        print('Hybrid cars in stock: ' + str(len(self.hybrid_cars)))
        

    def rentCar(self, car_list, amount, typecar, answ):
        if len(car_list) < amount and len(car_list) > 0:
            # the stock is not enough for the number of cars to rent
            # It is possible to rent the max number of cars left
            
            answ = input('The stock is not enough. Do you want proceed to rent '+str(len(car_list)) +
                         ' ' + typecar+ ' cars anyway? y/n \n')
            # If all the cars left are rented the list of cars is cleared
            if answ == 'y':
                car_list.clear()
                return
        elif len(car_list) == 0:
            # tehre are not cars in the list. Stock = 0
            print('There are not ' +typecar+ ' cars available at the moment.')
        elif len(car_list) > amount or len(car_list) == amount:
            total = 0
            while total < amount:
                car_list.pop()
                total = total + 1
           
    def returnCar(self, car_list, amount):
        total = 0
        while total < amount:
            car_list.append(1)
            total = total + 1

    def process_rental(self):
        answer = input('Would you like to rent a car R, return a car U, any key to quit?\n')
        # if the user has chosen to rent the method rentCar has been called for 
        #each type of car
        if answer == 'R':
            answ = ''
            typecar = input('What car would you like to rent - P for petrol, E for electric, D for diesel, H for hybrid?\n')
            amount = int(input('How many would you like renting?\n'))
            if typecar == 'P':
                self.rentCar(self.petrol_cars, amount, typecar, answ)
            elif typecar == 'E':
                self.rentCar(self.electric_cars, amount, typecar, answ)
            elif typecar == 'D':
                self.rentCar(self.diesel_cars, amount, typecar, answ)
            elif typecar == 'H':
                self.rentCar(self.hybrid_cars, amount, typecar, answ)
        # if the user has chosen to return the method returnCar has been called for
        # each type of car
        elif answer == 'U':
            typecar = input('What car would you like to return - P for petrol, E for electric, D for diesel, H for hybrid?\n')
            amount = int(input('How many would you like returning?\n'))
            if typecar == 'P':
                self.returnCar(self.petrol_cars, amount)
            elif typecar == 'E':
                self.returnCar(self.electric_cars, amount)
            elif typecar == 'D':
                self.returnCar(self.diesel_cars, amount)
            elif typecar == 'H':
                self.returnCar(self.hybrid_cars, amount)
                
        #return typecar
        self.stock_count()
        
    # The final stock  
    def save_csv(self):   
        csv_file = open('cars.csv', 'w')
        csv_file.write('Type, Stock\n')
        csv_file.write('P,' + str(len(self.petrol_cars)) + '\n')
        csv_file.write('E, ' + str(len(self.electric_cars)) + '\n')
        csv_file.write('D, ' + str(len(self.diesel_cars)) + '\n')
        csv_file.write('H, ' + str(len(self.hybrid_cars)) + '\n')
        csv_file.close()
     
if __name__ == '__main__':
    dealership = Dealership()
    dealership.create_current_stock('P',20)
    dealership.create_current_stock('E',6)
    dealership.create_current_stock('D',10)
    dealership.create_current_stock('H',4)
    proceed = 'y'
    while proceed == 'y':
        dealership.process_rental()
        proceed = input('Would you like to continue? y/n')
    dealership.save_csv()