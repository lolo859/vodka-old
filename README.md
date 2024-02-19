Vodka is a new experimental description language for creating different types of data in lines of code. Here are the types of codes currently supported as well as their designation:
- integer: vodkint
- float: vodfloat
- type (a special data type that can only store the type of a variable): vodtype
- raw text : vodtext
- text : vodstring

For creating a new object, type in a .vod file the following syntax:
vodka name_of_the_object_without_space = designation_of_the_data_type content

Example: vodka a = vodka 45

This will create a variable named a of type vodkint with a value of 45.

To display it, type:

vodprint a

This will display:

45

To export the variable to a .txt file, type:

vodexp name_of_the_variable absolute_path_to_the_file

To import a .txt file with a data type, type:

vodimp data_type name_of_the_variable_without_space absolute_path_to_the_file

To use a type's function :

vodka a = vodkint 123

vodka b = vodkint.lenght a

To convert variable, type :

vodka a = vodkint 45

vodka b = vodfloat.convint a

To store the type of a variable type :

vodka a = vodkint 45

vodka b = vodtype a

To display the Vodka version:

vodabout

To duplicate variable :

vodka a = vodkint 3

vodka b = vodka a

To create function named add.vodf :

VODSTART a b

vodka c = vodkint.add a b

VODEND c

To use this function :

VODSTART

vodfunc add

vodka a = vodkint 2

vodka b = vodkint 3

vodka c = add a b

VODEND

To comment :

VODSTART

vodabout § This will show the Vodka's version

VODEND
