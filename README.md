# Cloud_Compute_Base

This is a project for a basic framework of cloud computing

You may run it in server and access it using a browser.

setup login name to access the main page
The main page is just function chainning

We are not going to add function in this project, as it is just a basic framework.

There may be functions that are compatible for this framework in other project.


## Dependency:
 flask, opencv, numpy
 ## To Run
 To run the program, use the normal flask execution:
 python -m flask --app main run
 add --host=0.0.0.0 for opening to the lan and internet
 Then access the server by browser. The user name should be in config.ini file. Change it if you want. 

## UniApp
As mentioned before, it is a function chainning server. In first tab UniApp, you can chain function by
first click twice +number button and click one function button to add 2 number field and 1 function field, 
Then input number x, number y and add to the three input. Could be 1 -1 add. 
Finally click send, then you should see text: 0 in the result panel. To see more function, you should see the machine.py file. There are only a few functions as it is just framework. 

## File
file is a way to upload image to enable image processing function. Choose your file and a name and send it, you can then refer your image in uniapp, or ongoing mode. You can refer your image by $(variable) on a text field. A good example is 
$x(text) ->invertIm(text)->toIm. 
## Ongoing(Interactive)
It is a mode that you can do the operation step by step. It is just like a debug mode.
