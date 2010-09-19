The dotty-dots GAE Application:
-------------------------------------------------------------------------------
This is a python GAE app. Check out the docs here:
http://code.google.com/appengine/


Intro:
-------------------------------------------------------------------------------
The dotty-dots public website is a static HTML page (index.html) with a modified version of Rob Hawkes' Google bouncing-balls JavaScript that reads letter definitions from document.alphabet (defined in alphabet.js) instead of using the 'google' ball positions and coloring.

With index.html and the contents of the 'static' directory you can replicate the
dotty-dots public website.

The challenge was building and inputting that alphabet data, and that's what's 
covered below.

DISCLAIMER: This was hacked together in a couple of evenings, and provided 'warts-and-all' for you to use as you like. 


Creating the alphabet
-------------------------------------------------------------------------------
The process was:

1) secret-character-editor - edit:
There's a 'secret-character-editor' page at:
http://dotty-dots.appspot.com/secret-character-editor/edit.py?chr=A
(screenshot: http://img.skitch.com/20100909-b7r851rpxx92acmd8m9n89umrx.jpg)

Emile would change the character after '=' and enter the dots, move them, resize them, change the fades and save them to the datastore.

See app.yaml, edit.py for more details.


2) secret-character-editor - build alphabet.js:
Going to http://dotty-dots.appspot.com/secret-character-editor/alphabet.js
returns a javascript file that defines each letter, with the data as it appears
in our datastore.


3) Shape test area:
I set up http://dotty-dots.appspot.com/testarea/shapes.html
so that we could test how the characters would look using the latest letter definitions from the datastore.


4) Adjusting the fades:
It turns out fading wasn't consistent from letter to letter. Inside the 'color-analysis' folder you'll find a couple of scripts that I used to adjust the fades for each character.


5) Testing the fades:
I set up http://dotty-dots.appspot.com/testarea/fades.html to test out any new fades created by the color-analysis step.




Software credits:
-------------------------------------------------------------------------------
dotty-dots uses or adapts the following libraries and code:

 - Rob Hawkes Google bouncing-balls in HTML5:
   http://github.com/clawtros/google-bouncing-balls

 - A JavaScript slider control (on the character-editor)
   http://dhtmlx.com/docs/products/dhtmlxSlider/index.shtml

 - The simplejson python library
   http://pypi.python.org/pypi/simplejson/

 - An 'Unescaping' python function
   http://pypi.python.org/pypi/cgi.unescape 

 - jQuery
   http://jquery.com/

 - JSON2
   http://www.JSON.org/json2.js

 - Numpy/Matplotlib
   http://numpy.scipy.org/
   http://matplotlib.sourceforge.net/
