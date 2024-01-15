Vodka is a new experimental description language for creating different types of data in lines of code. Here are the types of codes currently supported as well as their designation:
- integer: vodkint
For creating a new object, type in a .vod file the following syntax:
vodka <name of the object without space> = <designation of the object type> <content>
Example: vodka a = vodka 45
This will create a variable named a of type vodkint with a value of 45.
To display it, type:
vodprint a
This will display:
45
To export the variable to a .txt file, type:
vodexp <name of the variable> <absolute path to the file>
To import a .txt file with a data type, type:
vodimp <data type> <name of the variable without space> <absolute path to the file>
To display the Vodka version:
vodabout
