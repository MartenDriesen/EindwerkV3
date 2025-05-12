from component_classes.Component import Component

class AC_Voltage_Src(Component):
    def __init__(self):
        super().__init__(image_path="./images/AC_voltage_source.png", size_x=40, size_y=80)
        self.pos_pin1 = None
        self.pos_pin2 = None
        self.name = "V"
        self.properties = [
            ["Voltage", 0],            
        ]