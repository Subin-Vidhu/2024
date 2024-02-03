from turtle import Turtle,Screen 
import random 

is_race_on=False 
#creating screen object
screen=Screen()
screen.setup(width=500,height=400)
screen.title("Welcome to the Turtle Race!")
# screen.bgcolor("aquamarine")   #setting background colour
choice=screen.textinput("Bet","Which turtle will win the race?Enter a colour:")


#set starting turtle's position to top left corner
posx=-230 
posy=150
#colours for all turtles
lis=["red","orange","yellow","green","blue","indigo","violet"]

#list of different turtle instances
race_turtles=[]

#creating multiple turtles and bringing them to starting positions
for x in range(7):
    new_turtle=Turtle(shape="turtle")
    new_turtle.color(lis[x])
    new_turtle.penup()    
    new_turtle.setposition(posx,posy) 
    race_turtles.append(new_turtle)
    posy-=50 

#only if user has placed a bet,while loop starts
if choice:
    is_race_on=True

while is_race_on:
    for turtle in race_turtles:
        rand_distance=random.randint(0,10)
        turtle.forward(rand_distance)

        if(turtle.xcor()>230):
            #turtle.color() returns pencolor and fillcolor
            winning_colour=turtle.pencolor()
            if(winning_colour==choice):
                print(f"You won the bet!The {winning_colour} turtle is the winner!")
            else:
                print(f"You lost!The {winning_colour} turtle is the winner!") 

            is_race_on=False



screen.exitonclick()