class Table:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height

class ComputerTable(Table):
    def __init__(self, **kwargs):
        '''
        doc
        '''
        super().__init__(kwargs['length'], kwargs['width'], kwargs['height'])
        self.shelf = kwargs.get('shelf', [10, 10])
    def square(self, comp_square):
        return(self.height * self.length - comp_square - self.shelf[0] * self.shelf[1])

table = ComputerTable(length = 100, width = 60, height = 70, shelf = [50, 30])
table_square = table.square(40)
print(f'Square {table_square}')