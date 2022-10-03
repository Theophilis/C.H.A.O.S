# C.H.A.O.S

###Cellular Haptic Automata Operating System: READ.ME

C.H.A.O.S (Chaos) is an interactive cellular automata exploration environment.Inside Chaos you can choose between binary, ternary, or quaternary cellular automata in one or two dimensions and dynamically change the rule applied to the data stream. The primary input method is key presses (currently statically mapped), although there is ample optionality for alternative methods/mappings and a rudimentary midi input option. 

The primary goal of Chaos is to create the widest variety of attribute manipulation tools for cellular automata. Through the use of these tools however, any method of artistic, intellectual, or spiritual exploration is encouraged and valued. I have found the true power of Chaos is not in the understanding of the automaton themselves, but in the understanding of what the automaton can teach you about you, your life, and the impact even the smallest change can have on complex systems.

---

Prerequisites: 

Source Code(latest versions implied):
  * Python
  * Pygame
  * Numpy
  * Os
  * Pickle
  * Datetime
  * Random
  
Portable:
* A relatively modern computer with a Windows or Mac operating system. (Sorry Linux, I’m not smart enough for you yet)

---

Installation:

Source Code:
* Download C.H.A.O.S folder
* Open .py files into IDE choice
* Import dependencies
* Enjoy

Portables:
* MAC
  * Download application 
  * Move to applications folder
  * Right click and press open
  * Assure MacOs that you trust the program
  * Launch and Enjoy

* Windows

    * Download installation package
    * Run and install into desired folders
    * Run .exe and enjoy

---

How to use:

Portable
  * The four green boxes on the left hand side of the screen (small, medium, large, X-large) choose the size of individual cells. Larger cell sizes will run better on slower/older computers.
  * The three red boxes on the right hand side (two, three, four) chose a binary, ternary, or quaternary automaton respectively. Each one has their own keybindings and behaviors. A full exploration of all three is encouraged because many of the themes present in the smaller based automaton (binary and ternary) become the building blocks for the more exciting manifestations possible. 
  * The purple box in the bottom right hand side of the menu is the speed setting. Integers between 1-10 tend to produce the best results and maximize visual cohesiveness. My preferred speed is around 4-6. 
  * Once a Cell Size, Number of Colors and Speed is chosen click the blue enter button on the bottom of the screen to start the cellular automaton generation
  

* Key Mapping:
  * Binary
    * Keys -a s d f j k l ;- correspond to the eight output choices in a binary cellular automata. Key presses alternate the values of the chosen rule position between 0 & 1
      * Example:
        * Decimal rule: 90
        * Binary rule: [0, 1, 0, 1, 1, 0, 1, 0]
        * Key map:    [a, s, d,  f,  j,  k,  l,  ;]
        * Keypress:   [a]
        * New Binary rule: [1, 1, 0, 1, 1, 0, 1, 0]
        * Keypress:   [s]
        * New Binary rule: [1, 0, 0, 1, 1, 0, 1, 0]
        
  * Ternary
    * The full qwerty alphabet and the space bar correspond to one of the 27 output choices in a ternary cellular automata. Key presses alternate the values of the chosen rule position between 0,1 & 2 
    * Example:
      * Decimal rule: 21621
      * Ternary rule: [000000000000000001002122210]
      * Key map:      [qwertyuiopasdfghjklzxcvbnm_]
      * Keypress:     [q]
      * New Ternary rule: [100000000000000001002122210]
      * Keypress:     [q]
      * New Ternary rule: [200000000000000001002122210]
      * Keypress:     [w]
      * New Ternary rule: [210000000000000001002122210]
    
  * Quaternary
    * The Full qwerty alphabet and the space bar correspond to a value between 1-27,  and each key press has a keypress counter. The keypress counter is given to a mod 3 function (subtracting one form the result), then multiplied by 27, added to the key presses native value, and then given to a mod 64 function to correspond to one of the 64 output choices in a quaternary cellular automata. Final keypress values alternate the values of the chosen rule position between 0, 1, 2 & 3
      * Example:
        * Quaternary Rule: [0…0]
        * Key map: same as ternary
        * Keypress: [q] count = 1
        * Keypress value = 0 + (((count % 3) - 1) * 27) % (64) = 0
        * Quaternary Rule: [1…0]
        * Keypress: [q] count = 2
        * Keypress value = 0 + (((count % 3) - 1) * 27) % (64) = 27
        * Quaternary Rule: [1…1…0]
        * Keypress: [q] count = 3
        * Keypress value = 0 + (((count % 3) - 1) * 27) % (64) = 54
        * Quaternary Rule: [1…1…1…0]
        * Keypress: [q] count = 4
        * Keypress value = 0 + (((count % 3) - 1) * 27) % (64) = 0
        * Quaternary Rule: [2…1…1…0]
        
---

Source Code:
* Chaos has two main parts. The first is the graphical interface; consisting of the main menu and Chaos window. These two parts serve to reduce the barrier to entry for attribute manipulation and apply color and movement to the underlying cellular automaton generation. The Second is the actual cellular automata engine. This takes the base of the desired automata (binary, ternary, quaternary), cell size parameters(small, medium, large, X-large), initial rule, and initial row values, in order to continuously apply the rules and generate an arbitrarily long cellular automata, whose rules are dynamically adjusted by key presses (described in the portable section).

Graphical interface:

* The GUI is built using pygame.
* The main menu consists of eight buttons, one value input box, and various text descriptions.
    * The buttons are built from two rectangles (one colored one black), and a label
    * Button presses are detected through a combination of mouse collision and mousebutton_1 clicking.
    * There are Three classes of buttons
      * ‘Cell Size’
      * ‘Number of Colors’
      * ‘Enter’
      * Cell Size, and Number of Colors, when pressed, changes a variable that is then passed to the Chaos_Window.
      * A button's text also flashes white when pressed to give positive feedback for actions.
      * The ‘Cell Size’ buttons, small, medium, large, X-large, pass values of 2, 3, 5, 10 respectively to the pixel_res variable. This variable is used in the Chaos_Window to choose the size of the cell's png.
      * Variable values and image resolutions are one to one.
      * The ‘Number of Colors’ buttons (two, three, four) pass identical values to the base variable. This variable is used in the Chaos_Window to decide how many different cell colors need to be used, and is passed to the cellular automaton generator to receive the appropriate rules, and row values.
      * The Enter button calls the Choas_Window function with three variables, base, pixel_res, cell_vel.
    * Inputs:
      * The input field is built from two rectangles (one colored one black)
      * The field (vel_rect) is activated once a collision is detected between the mouse and the box area.
      * Upon activation the word ‘Speed:’ will appear to show a readiness for inputs.
      * The field only recognized integer inputs from 0-9.
      * The inputs are passed to a string and a backspace keypress cuts off the last digit entered.
      * Once the mouse is no longer colliding with the vel_rect area the string is converted to an integer value ‘cell_vel’ and passed to the Chaos_Window.
      

* Chaos_Window:
  * Chaos_Windows primary function is to take the raw calculations of the cellular automata generation and create a graphical representation for it.
  * Chaos_Window has four parts. Two functions, redraw_window and mitosis, a pixel class and a primary while loop.
    * Functions:
      * Redraw_window:
        * Redraw window is called to update the screen position for the cells, the rule label, the step count, and the randomize counter.
      * Mitosis:
        * Inputs:
          * I
            * Cell row position
          * R
            * Cell row value
          * Color
            * List with the index values for a cell whose evolution value isn’t 0
          * Rc
            * ‘Rule Call’ list of values which correspond to the rule position called by the last step in the cellular automaton evolution.
          * Row
            * Current row of the cellular automata
          * Pixel_res
            * Variable passed from Green buttons in the main menu
        * The Mitosis function is called to populate a new row in the evolution of the cellular automata with cells.
        * Mitosis has two primary paths, r>0 and else(r==0)
          * Inside each of the paths there are five options for how the new row is to be populated. 
            * R_c == 1: & r_c == 2: use the rc list to populate a cell row according to which rule position was called in the evolution of the automaton.
            * Base == 2/3/4: use the row values to populate a cell row.
          * Cell rows are populated by adding new instances of the Cell class to the cells list. The only difference between cells in the list is the color designated by cellular evolution.
      * Pixel:
        * Pixel class has an x and y positional value and three functions. 
        * Draw: draws pixels on the screen according to the x and y values.
        * Get_width & get_height return the current x and y values of the object.
        * Pixel has one subclass Cell with an extra color attribute and a move function.
          * Cells move function takes one velocity parameter and uses it to adjust the Cells y value.
      * Main Loop:
        * There are four parts to the Main loop. The first part is responsible for populating the cells list with new rows, the second part preps the rule variable for data collection, the third part handles key presses, and the fourth updates the position of the cells.
        * 1:
          * For each row in the cells list the Color_cells function is called giving the color, rc, and row variables.
          Then the row and rc are checked against the current record of prior rows. If a row has been generated before then the rules are changed at random until a unique row is found.
          If the row is unique it is recorded in the journal and each cell in the row is passed to mitosis.
        * 2:
          * The current rule list is turned into a string and attached to a timestamp for journal entries.
        * 3:
          * Each base has their own key press definitions described in the portable section
        * 4:
          * Each cell in each row has their position updated. If their y value is equal to the length of the screen they are deleted. 

---

Chaos engine:
  * The Cellular automata is generated using four functions, base_x, rule_gen, viewer, and Color_cells.
  * Base_x:
    * Base_x takes two inputs
      * N:
        * The decimal integer being converted
      * B
        * The base for desired conversion
    * By taking recursive logs it returns a string of the desired conversion
  * Rule_gen:
    * Rule_gen takes two inputs.
      * Rule:
        * The base_x value for the current value.
      * Base
        * The base of the automata
    * Rule_gen pairs each value in the base_x representation of the rule with the base_x version of its index value in a dictionary.
      * Example:
        * Rule: 90
        * Base: 2
        * base_rule = [0,1,0,1,1,0,1,0]
        * Index_rule = {7:0, 6:1, 5:0, 4:1, 3:1, 2:0, 1:1, 0:0}
        * (Final) dict_rule = {111:0, 110:1, 101:0, 100:1, 011:1, 010:0, 001:1, 000:0}
  * Viewer:
    * Viewer takes four inputs.
      * Row
        * Current row in the cellular automata
      * Y
        * Index position in the current row
      * View
        * Size of the view window
      * V_0
        * Empty list where the desired section of the row is placed
    * Viewer recursively creates a d_rule compatible list of a view length size. The cells included in v_0 are immediate neighbors of the cell in the index position. Cells are added to v_0 in a right-left alternating fashion.
    * If the view size is larger than any given index position will allow (usually first or last in a row) then zeros are used to fill in v_0 until it reaches the desired size.
    * Example:
      * Row: [1, 1, 0, 0, 1, 0, 0, 0, 0]
      * Y = 4
      * View = 3
      * V_0 = [0, 1, 0]
      * Y = 3
      * V_0 = [0, 0, 1]
      * Y = 0
      * V_0 = [0, 1, 1]
  * Color_cells:
    * Color_cells takes five inputs:
      * Color
        * A list of index position of non zero values in the prior row
      * D_rule
        * Dictionary of all possible view windows and their corresponding values according to the current rule.
      * Cell_row_width
        * Number of cells in a row
      * Base
        * Base of the cellular automata
      * Row_0
        * Row to be iterated on 
    * Color_cells creates a new row by iterating across the old row with the viewer, and applying the d_rule[v_0] value to the row_1 array, and the d_rule[v_0] index position to the rc list

---

Contributions:
* All contributions are welcome. I have never published on GitHub before, so please be patient, explain your changes thoroughly, and be ready for some questions about implementation. Thank you for choosing to spend your time here, this project has had a profound impact on my life, and I want is to share the experience with as many people as possible.

Contact:
* you can reach me at chaotomata@gmail.com

License:
* This project is protected under the GNU General Public License v3.0