from component_classes.Component import Component

class feedbackBlock(Component):
   def __init__(self):
        super().__init__(image_path = "./images/feedback.png", size_x = 20, size_y = 20)
        self.feedback = ""
        self.pos_pin1 = None 
        self.pos_pin2 = None
        self.name = "Fe"

        
