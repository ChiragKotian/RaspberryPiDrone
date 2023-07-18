# Raspberry Pi Drone Steps and ROS
In this project we integrated Raspberry Pi and ROS with drone to explore various ways it can be controlled and various other aspects.

## Some good softwares to use with Ubuntu Server version:
1. **Vim (Text Editor which is like an IDE)**:

    You can use ```$ vimtutor``` to start an inbuilt tutorial, which is pretty detailed and comprehensive. _(See bottom of terminal to know the mode you are in)_.


   Here, we will try to give you some notes we made from the tutorial.

   1. **To _Open_ a file for editing**: ```vim "file_name"``` (_Enter your file name in place of "file_name" on terminal_) (**_If there is no file of the provided name in current directory, then a 'NEW' file will be created_**)
   2. **To _Save_ and _Exit_**: ```:wq```

   Once in Vim editor, you first press some keys to enter a mode and then to the changes to the text based on the mode you are in.
  
      1. **To navigate, use**: ```h```(left) ```j```(down) ```k```(up) ```l```(right) or 'arrow' keys.  
      2. **To exit without savin**g: ```:q!```
      3. **To delete text**: ```x```
      4. **Enter _Normal_ mode**: 'esc' key
      5. **_Insert_ text mode**(_Inserts text behind the current position of cursor_): ```i```
      6. **_Append_ text mode**(_Inserts text ahead of the current position of cursor_): ```a```
      7. **To _Save_ and _Exit_**:

3. **Tmux(Multiwindow terminal with facilitates easy switching and other functions)**

