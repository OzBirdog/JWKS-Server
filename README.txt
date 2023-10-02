JWKS Server Project
CSCE 3550.001
Oz Birdett (oeb0010)
10-1-2023

Description: The following repository contains the files, jwksServer.py and testSuite.py, for the JWKS Server Project. As well as screenshots showing the results of both the test suite and the test client being run with the JWKS Server. Both files are written in Python and use Flask for the web server. The jwksServer.py file is a server that provides public keys with unique identifiers for verifiying JSON Web Tokens. The keys are generated using RSA, have an expiration, and authentication endpoint. The testSuite.py file has three test cases to run against the JWKS Server to check the test coverage.

Execution:

For test coverage:

Run jwksServer.py in one terminal
Run testSuite.py in another terminal
Check results in terminal of testSuite.py

For test client:

Run jwksServer.py
Run gradebot from test client repository
Check results in terminal of jwksServer.py
