from component_classes.Component import Component

class Triac(Component):
    def __init__(self):
        super().__init__(image_path="./images/Triac.png", size_x=60, size_y=80)
        self.pos_pin1 = None
        self.pos_pin2 = None
        self.pos_pin3 = None
        self.name = "S"
        self.properties = [
            ["Max blocking voltage", 0], 
            ["Gate trigger current", 0],    
            ["Holding current", 0],   
            ["Max surge current", 0],            
        ]
