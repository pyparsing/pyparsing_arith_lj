#
# shape_commands.py
#
# Example of attaching evaluator classes as parse actions, for simple shape drawing.
#
# Copyright(c) 2017, Paul McGuire
#
import pyparsing as pp
import turtle

"""
BNF:
    shape_command ::= circle_command | square_command
    circle_command ::= 'circle' xy_coord integer
    square_command ::= 'square' xy_coord integer
    xy_coord ::= integer integer
    integer ::= '0'..'9'+
"""

integer = pp.pyparsing_common.integer

# coordinate pair - assign names for parsed results
x_y_coord = pp.Group(integer("x") + integer("y"))

# commands to create specific shapes
circle_cmd = pp.CaselessKeyword("circle") + x_y_coord("center") + integer("radius")
square_cmd = pp.CaselessKeyword("square") + x_y_coord("upper_left") + integer("side_length")
# Extra credit!
hexagon_cmd = pp.CaselessKeyword("hexagon") + x_y_coord("center") + integer("radius")

shape_command = circle_cmd | square_cmd | hexagon_cmd

# classes to be constructed by parser from parsed commands
class Shape(object):
    def draw(self):
        raise NotImplementedError()
    def __repr__(self):
        return "{}:({})".format(self.__class__.__name__, self.tokens.asDict())

class Circle(Shape):
    def __init__(self, tokens):
        self.tokens = tokens
        self.center = tokens.center
        self.radius = tokens.radius
    
    def draw(self):
        turtle.penup()
        turtle.goto(self.center.x, self.center.y)
        turtle.pendown()
        turtle.circle(self.radius)

class Square(Shape):
    def __init__(self, tokens):
        self.tokens = tokens
        self.upper_left = tokens.upper_left
        self.side_length = tokens.side_length
    
    def draw(self):
        turtle.penup()
        turtle.goto(self.upper_left.x, self.upper_left.y)
        turtle.setheading(0)
        turtle.pendown()
        for i in range(4):
            turtle.forward(self.side_length)
            turtle.right(90)

class Hexagon(Shape):
    def __init__(self, tokens):
        self.tokens = tokens
        self.center = tokens.center
        self.radius = tokens.radius

    def draw(self):
        turtle.penup()
        turtle.goto(self.center.x, self.center.y+self.radius)
        turtle.setheading(-30)
        turtle.pendown()
        for i in range(6):
            turtle.forward(self.radius)
            turtle.right(60)

# attach classes to command expressions as parse actions
circle_cmd.addParseAction(Circle)
square_cmd.addParseAction(Square)
hexagon_cmd.addParseAction(Hexagon)

# accept multiple commands to create multiple shapes
parser = pp.OneOrMore(shape_command)

# test parser on some sample commands
sample_commands = """\
    circle 100 100 20 
    square 50 50 10
    hexagon 50 100 30
"""
shapes = parser.parseString(sample_commands)

# print generated Shape instances
print(shapes)

# walk the list of Shape instances and call draw() on each
for shape in shapes:
    shape.draw()

# wait for user to press <ENTER>, else turtle panel will close immediately
input('Press <ENTER> to continue...')
