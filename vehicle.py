class Vehicle:
    def __init__(self, brand, color):
        self.brand = brand
        self.color = color
        self.speed = 0

    def acelerar (self):
        self.sleed += 10
        print(f"El {self.brand} aceleró a {self.speed} km/h")

        #creación de los objetos
        my_vehicle = Vehicle('Hiunday', 'Black')
        my_vehicle.acelerar()
        my_vehicle.acelerar()
        my_vehicle.acelerar()
