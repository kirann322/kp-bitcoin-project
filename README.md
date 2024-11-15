# kp-bitcoin-project

## Overview
This repository contains an implementation of various components of bitcoin and is split out into distinct classes that try to encapsulate various components and/or concepts which are relevant in the implementation of bitcoin and cryptocurrencies in general. Each class represents a distinct set of functionalities which are bundled together and also have a set of unit tests associated with them to ensure proper functionality. There are currently a total of 10 sub components of this implementation, listed below,

- elliptic curve cryptography
	- finite fields
	- elliptic curves
	- secp256k1
	- digital signature algorithms
- transactions
- script with op codes
- blocks
- networking
- merkle trees
- bloom filters

The src folder contains each of these classes, which define the some of core operations that are necessary to build a functional cryptocurrency. The tests folder contains a variety of unit tests for each class and can be run to ensure their proper functionality.

## How to run tests and verify functionality
1) Download and install python3, via https://www.python.org/downloads/
2) Use pip to install pipenv, via the command `pip install pipenv`
3) Clone the repository using `git clone <repo-address>`
4) Navigate to the repository using `cd kp-bitcoin-project`
5) Run `pipenv install`, this should install the packages needed to run the tests in a new virtual environment
6) Run each of the unit tests in the test folder and ensure they pass
