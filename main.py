from fa import *
from os import system
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def menu():

    auto1 = DFA()
    auto2 = DFA()

    equivalence = []

    input_filename = None
    output_filename = None

    while True:
        print("\n\nMenu")
        print("1. Read data from a DFA")
        print("2. Minimize a DFA")
        print("3. Write a minimized DFA")
        print("4. Process a given word")
        print("   Press q to exit")

        option = input("Choose an option: ")

        system('cls')

        if option == '1':

            # read the input file   
            root = Tk()
            # we don't want a full GUI, so keep the root window from appearing
            root.withdraw() 
            # move the window in focus
            root.lift()
            root.attributes("-topmost", True)
            # file asking
            filename = askopenfilename(filetypes=(('Text files', '*.txt'),)) # show an "Open" dialog box and return the path to the selected file
            
            if filename == '':
                print("No file selected!")

            else :
                auto1.read_from(filename)
                input_filename = filename
                print("DFA read!")
        
        elif option == '2':

            if len(auto1.nodes) == 0:
                print("No DFA read!")
            else:
                equivalence = auto1.minimization()
                print("DFA minimized")
        
        elif option == '3':
            
            if len(auto1.nodes) == 0:
                print("No DFA read")
            else:
                print(equivalence)
                output_filename = input("Enter the output filename: ")
                auto1.write_to_file(output_filename, equivalence)

                auto2.read_from(output_filename)
                print("DFA minimized read!")
        
        elif option == '4':
            
            if len(auto2.nodes) == 0:
                print("No minimized version to compare!")
            else:
                
                auto1 = DFA()
                auto2 = DFA()

                auto1.read_from(input_filename)
                auto1.minimization()
                auto1.write_to_file(output_filename, equivalence)

                auto2.read_from(output_filename)

                word = input("Enter a word to check: ")

                print("Original DFA:")
                auto1.validate_word(word)
                print("Minimized DFA:")
                auto2.validate_word(word)

        elif option == 'q':
                exit(0)

        else:
            print("Enter a valid option!\n")


if __name__ == '__main__':
     menu()
