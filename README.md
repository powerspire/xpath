# xpath
Scans a web page and creates xpath expressions to uniquely locate objects
The xpath can then be used to write selenium tests.
If more than 1 object has the same attributes, it tries to find an ancestor element so it can create a unique xpath expression for the object


Known Issues
1. hrefs with relative paths return the full URL in the expression 
2. Text with quotes and apostrophes can cause the expression to be invalid