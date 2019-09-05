For working directly with the DRT.
Configuration elements of the DRT
    - Upper ISI : the upper range of time that the next stim will happen. use upperISI in command
        range: 0-int.maxvalue
    - Lower ISI : the lower range of time that the next stim will happen. use lowerISI in command
        range: 0-int.maxvalue
    - Stim Duration : the length of time the next stim will remain for. use stimDur in command
        range: 0-int.maxvalue
    - Stim intensity : the intensity of the next stim. use intensity in command
        range: 0-255

Use get or set followed by underscore followed by an element to form a command. Any get command takes no arguments,
any set command takes one value argument in the form of an integer separated from the command by a space.
    - example of a get command : "get_lowerISI"
    - example of a set command : "set_stimDur 255"