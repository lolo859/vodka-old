Vodka is a new experimental description language for creating different types of data in lines of code. Here are the types of codes currently supported as well as their designation:
- integer: vodkint

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

To display the Vodka version:

vodabout
