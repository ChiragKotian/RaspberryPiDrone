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
      9. **Vim functions have _Operators_, _Count_ and _Motions_, like**:
          
         1. ```d``` <- _Operator_  (Tells the operation to be carried out, in this case delete)
  
         2. ```2/3/4...``` <- _Count_ (Tells how many times to repeat an operation)_(Without count a operation is carried out once)_
            
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
   12. **To _Put Back_ text that has just been deleted**: ```p``` _(This puts the deleted text after the cursor, if a line was deleted(```dd```)(Only one line is stored in Vim register), it will go on the line below the cursor)_
   13. **To _Replace_ the character under the cursor**: ```r``` and _then type the character you want to replace it with_
   14. **_Change_ operator**: ```c``` (Change deletes a piece of text based on motion and then sends you into Insert mode so that you can continue typing, changing the original text into something else)
   15. **Show current _File Location_ and it's _Status_**: ``` ctrl + G```
   16. **Move**:
       
        1. _End of file_: ```G```
        2. _To first line_: ```gg```
        3. _To specified line_: ``` "line number" + G```

    17. **Find _Phrases_**:
        1. _Search forward_: ```/ + "phrase"```
        2. _Search backward_: ```? + "phrase"```
        3. _Occurrence in the same direction_:
           
           1. _Next_: ```n```
           2. _Previous_: ```N```

    18. **Go to a _Position of Yours_**:
        
        1. _Older_: ```ctrl + O```
        2. _Newer_: ```ctrl + I```

    19. **Debug missing brackets ( (,);[,];{,} )**: ```%``` (_While cursor on one of it takes you to it's match_)
    20. 
         

3. **Tmux(Multiwindow terminal with facilitates easy switching and other functions)**

##MAVROS COMMANDS (MAVCMD):
1. **PARAMETERS**:
   
   1. 0: HEARTBEAT
   2. 1: SYS_STATUS
   3. 2: SYSTEM_TIME
   4. 4: PING
   5. 5: CHANGE_OPERATOR_CONTROL
   6. 6: CHANGE_OPERATOR_CONTROL_ACK
   7. 7: AUTH_KEY
   8. 11: SET_MODE
   9. 20: PARAM_REQUEST_READ
   10. 21: PARAM_REQUEST_LIST
   11. 22: PARAM_VALUE
   12. 23: PARAM_SET
   13. 24: GPS_RAW_INT
   14. 25: GPS_STATUS
   15. 26: SCALED_IMU
   16. 27: RAW_IMU
   17. 28: RAW_PRESSURE
   18. 29: SCALED_PRESSURE
   19. 30: ATTITUDE
   20. 31: ATTITUDE_QUATERNION
   21. 32: LOCAL_POSITION_NED
   22. 33: GLOBAL_POSITION_INT
   23. 34: RC_CHANNELS_SCALED
   24. 35: RC_CHANNELS_RAW
   25. 36: SERVO_OUTPUT_RAW
   26. 37: MISSION_REQUEST_PARTIAL_LIST
   27. 38: MISSION_WRITE_PARTIAL_LIST
   28. 39: MISSION_ITEM
   29. 40: MISSION_REQUEST
   30. 41: MISSION_SET_CURRENT
   31. 42: MISSION_CURRENT
   32. 43: MISSION_REQUEST_LIST
   33. 44: MISSION_COUNT
   34. 45: MISSION_CLEAR_ALL
   35. 46: MISSION_ITEM_REACHED
   36. 47: MISSION_ACK
   37. 48: SET_GPS_GLOBAL_ORIGIN
   38. 49: GPS_GLOBAL_ORIGIN
   39. 50: SET_LOCAL_POSITION_SETPOINT
   40. 51: LOCAL_POSITION_SETPOINT
   41. 52: GLOBAL_POSITION_SETPOINT_INT
   42. 53: SET_GLOBAL_POSITION_SETPOINT_INT
   43. 54: SAFETY_SET_ALLOWED_AREA
   44. 55: SAFETY_ALLOWED_AREA
   45. 56: SET_ROLL_PITCH_YAW_THRUST
   46. 57: SET_ROLL_PITCH_YAW_SPEED_THRUST
   47. 58: ROLL_PITCH_YAW_THRUST_SETPOINT
   48. 59: ROLL_PITCH_YAW_SPEED_THRUST_SETPOINT
   49. 60: SET_QUAD_MOTORS_SETPOINT
   50. 61: SET_QUAD_SWARM_ROLL_PITCH_YAW_THRUST
   51. 62: NAV_CONTROLLER_OUTPUT
   52. 63: SET_QUAD_SWARM_LED_ROLL_PITCH_YAW_THRUST
   53. 64: STATE_CORRECTION
   54. 65: RC_CHANNELS
   55. 66: REQUEST_DATA_STREAM
   56. 67: DATA_STREAM
   57. 69: MANUAL_CONTROL
   58. 70: RC_CHANNELS_OVERRIDE
   59. 73: MISSION_ITEM_INT
   60. 74: VFR_HUD
   61. 75: COMMAND_INT
   62. 76: COMMAND_LONG
   63. 77: COMMAND_ACK
   64. 81: MANUAL_SETPOINT
   65. 82: SET_ATTITUDE_TARGET
   66. 83: ATTITUDE_TARGET
   67. 84: SET_POSITION_TARGET_LOCAL_NED
   68. 85: POSITION_TARGET_LOCAL_NED
   69. 86: SET_POSITION_TARGET_GLOBAL_INT
   70. 87: POSITION_TARGET_GLOBAL_INT
   71. 89: LOCAL_POSITION_NED_SYSTEM_GLOBAL_OFFSET
   72. 90: HIL_STATE
   73. 91: HIL_CONTROLS
   74. 92: HIL_RC_INPUTS_RAW
   75. 93: HIL_ACTUATOR_CONTROLS
   76. 100: OPTICAL_FLOW
   77. 101: GLOBAL_VISION_POSITION_ESTIMATE
   78. 102: VISION_POSITION_ESTIMATE
   79. 103: VISION_SPEED_ESTIMATE
   80. 104: VICON_POSITION_ESTIMATE
   81. 105: HIGHRES_IMU
   82. 106: OPTICAL_FLOW_RAD
   83. 107: HIL_SENSOR
   84. 108: SIM_STATE
   85. 109: RADIO_STATUS
   86. 110: FILE_TRANSFER_PROTOCOL
   87. 111: TIMESYNC
   88. 112: CAMERA_TRIGGER
   89. 113: HIL_GPS
   90. 114: HIL_OPTICAL_FLOW
   91. 115: HIL_STATE_QUATERNION
   92. 116: SCALED_IMU2
   93. 117: LOG_REQUEST_LIST
   94. 118: LOG_ENTRY
   95. 119: LOG_REQUEST_DATA
   96. 120: LOG_DATA
   97. 121: LOG_ERASE
   98. 122: LOG_REQUEST_END
   99. 123: GPS_INJECT_DATA
   100. 124: GPS2_RAW
   101. 125: POWER_STATUS
   102. 126: SERIAL_CONTROL
   103. 127: GPS_RTK
   104. 128: GPS2_RTK
   105. 129: SCALED

