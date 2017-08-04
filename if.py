number = 23
guess = int(input("Enter an integer:"))

if guess == number:
    print('Congratulations,you guessed it.')
    print('The number is {0}'.format(number))
elif number < guess:
    print('Your input number is bigger than that')
else:
    print('Your input is smaller than that')
print('Done')