from direct.showbase.ShowBase import ShowBase

class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # Load your car model
        self.car = self.loader.loadModel("models/car.obj")
        self.car.reparentTo(self.render)
        self.car.setPos(0, 10, 0)
        
        # Might need to scale it (models come in different sizes)
        self.car.setScale(0.1, 0.1, 0.1)  # Make it smaller
        # OR
        self.car.setScale(5, 5, 5)  # Make it bigger

game = MyGame()
game.run()