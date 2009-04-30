import os
import os.path

class Controller:
    
    def __init__(self, file):
        self.file = file
        pass

    def start(self):
        f = open(self.file, 'w').close()

    def stop(self):
        os.remove(self.file)

    def is_start(self):
        return os.path.exists(self.file)

if __name__ == '__main__':
    pass
