Application purpose: 
To build an api that consumes a list of source address, destination address and content then send for each a submit_sm request under smpp protocol 

Application structure:
The application is implemented in python using flask Framework
For smpp client, the library used is smpp_lib (https://github.com/python-smpplib/python-smpplib) 

Api path: /messages
Api request sample: 
[
    { "dst_number": "70499753", "content": "Hello","source_number":"71696636"},
    { "dst_number": "70499753", "content": "Hello","source_number":"71696680"}
  
]