import re                                       #imports regular expressions library to use in 2nd and 3rd function.
from sympy import Matrix, lcm                   #from the library sympy imports Matrix, for the element table list and
                                                #the lcm, Lowest Common Multiplication, function of the sympy library
                                                #for the balancing part.

def main():                                     #Defines the main program. It contains 3 major functions
    elementList = []
    elementMatrix = []
    print("please input your reactants")
    reactants = input("Reactants: ")
    print("please input your products")
    products = input("Products: ")
    reactants = reactants.replace(' ', '').split("+")
    products = products.replace(' ', '').split("+")



    def addToMatrix(element, index, count, side):       #1st major function. Locates which column we want to modify by
                                                        #using the index function on element list. Modifies
                                                        #elementMatrix at the index and column position and increment it
                                                        #by the product of element count and the side to give the
                                                        #correct sign.
        if (index == len(elementMatrix)):
            elementMatrix.append([])
            for x in elementList:
                elementMatrix[index].append(0)
        if (element not in elementList):
            elementList.append(element)
            for i in range(len(elementMatrix)):
                elementMatrix[i].append(0)
        column = elementList.index(element)
        elementMatrix[index][column] += count * side



    def findElements(segment, index, multiplier, side):                 #2nd major function. Recognizes and seperates
                                                                        #each element Separates out the elements
                                                                        #and numbers using a regex and looping through
                                                                        #every element.
        elementsAndNumbers = re.split('([A-Z][a-z]?)', segment)
        i = 0
        while (i < len(elementsAndNumbers) - 1):
            i += 1
            if (len(elementsAndNumbers[i]) > 0):                        #Checks if the length of the segment is greater
                                                                        #than zero, because we will have some blanks.
                                                                        #If it is greater than zero, we want to check
                                                                        #if the one after it is non-zero.
                if (elementsAndNumbers[i + 1].isdigit()):
                    count = int(elementsAndNumbers[i + 1]) * multiplier
                    addToMatrix(elementsAndNumbers[i], index, count, side)
                    i += 1
                else:
                    addToMatrix(elementsAndNumbers[i], index, multiplier, side)

    def compoundDecipher(compound, index, side):                    #3rd major function. This def seperates parentheses
                                                                    # and loops each segment

        segments = re.split('(\([A-Za-z0-9]*\)[0-9]*)', compound)   # seperates the outermost parentheses. Also
                                                                    # indicates we are okay with any letter, of any
                                                                    #case, and that we want to include all numbers in
                                                                    #the split

        for segment in segments:                                    #Loops the segments
            if segment.startswith("("):
                segment = re.split('\)([0-9]*)', segment)
                multiplier = int(segment[1])
                segment = segment[0][1:]
            else:
                multiplier = 1
            findElements(segment, index, multiplier, side)

    # The main program starts here
    for i in range(len(reactants)):
        compoundDecipher(reactants[i], i, 1)
    for i in range(len(products)):
        compoundDecipher(products[i], i + len(reactants), -1)
    elementMatrix = Matrix(elementMatrix)
    elementMatrix = elementMatrix.transpose()
    solution = elementMatrix.nullspace()[0]
    multiple = lcm([val.q for val in solution])
    solution = multiple * solution
    coEffi = solution.tolist()
    output = ""
    for i in range(len(reactants)):
        output += str(coEffi[i][0]) + reactants[i]
        if i < len(reactants) - 1:
            output += " + "
    output += " -> "
    for i in range(len(products)):
        output += str(coEffi[i + len(reactants)][0]) + products[i]
        if i < len(products) - 1:
            output += " + "
    print(output)

    #Loops the program for unlimited potential uses.
    Repeat = input("Do you want to balance another chemical reaction?")
    if Repeat == "Yes" or Repeat == "yes":
        main()
    else:
        quit()
main()