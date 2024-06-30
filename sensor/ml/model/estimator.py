class TargetValueMapping:
    def __init__(self):
        self.neg : int = 0
        self.pos : int = 1
    
    def to_dict(self):
        return self.__dict__
    
    def reverse_mapping(self):
        return {v:k for k,v in self.to_dict().items()}