# Raspberry Pi Drone Steps and ROS
In this project we integrated Raspberry Pi and ROS with drone to explore various ways it can be controlled and various other aspects.

## Some good tools to use with the Ubuntu Server edition version or Ubuntu terminal in general:
1. **Vim (Text Editor, which is like an IDE)**:

    You can use ```$ vimtutor``` to start an inbuilt tutorial, which is pretty detailed and comprehensive. _(See bottom of terminal to know the mode you are in)_. 


   Here, we will try to give you some notes we made from the tutorial.

   1. **To _Open_ a file for editing**: ```vim "file_name"``` (_Enter your file name in place of "file_name" on terminal_) (**_If there is no file of the provided name in the current directory, then a 'NEW' file will be created with the given name_**)
   2. **To _Save_ and _Exit_**: ```:wq```

   Once in Vim editor, you first press some keys to enter a mode and then do the changes to the text based on the mode you are in.
  
      1. **To navigate, use**: ```h```(left) ```j```(down) ```k```(up) ```l```(right) or 'arrow' keys.  
      2. **To exit without savin**g: ```:q!```
      3. **To delete text**: ```x```
      4. **Enter _Normal_ mode**: 'esc' key
      5. **_Insert_ text mode**(_Inserts text behind the current position of cursor_): ```i```
      6. **_Append_ text mode**(_Inserts text ahead of the current position of cursor_): ```a```
      7. **To _Delete one word_**: Go to the start of the word and type ```dw```
      8. **To _Delete all the trailing characters after a character including the character_**: Go to the start of character and type ```d$```
      9. **Vim functions have _Operators_, _Numbers_ and _Motions_, like**:
          
         1. ```d``` <- _Operator_  (Tells the operation to be carried out, in this case delete)
  
         2. ```2/3/4...``` <- _Number_ (Tells how many times to repeat an operation)_(Without number a operation is carried out once)_
            
         3. ```w/$/e/d``` <- _Motion_ (Tells what to operate on)
        
             1. ```w``` <- _Until the start of the next word, excluding its first character_

             2. ```$``` <- _To the end of the line, including the last character_
             
             3. ```e``` <- _End of current word including last character_
             
             4. ```d``` <-  _Entire line_ (Example: ```dd``` deletes the whole line)
           
         Examples: ```d2w``` _deletes_ two words, ```2w``` _moves_ two words forward, ```3e``` _moves_ three words forward but at the last letter of the third word, ```0``` gets you to the _start_ of the word
         
   10. **To _Undo_**:
         
                 1. _Last command_: ```u```
                 2. Bring _whole line_ to original form: ```U```
                    
   11. **To _Undo the Undo_**: ```ctrl + R ```
           
         

3. **Tmux(Multiwindow terminal with facilitates easy switching and other functions)**

