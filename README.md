# MPI-Programming-Project
# CMPE 300 - Analysis of Algorithms Fall 2022 

This program is an implementation of MPI (Message Passing Interface) library in Python. The program uses MPI library to parallelize the text analysis of a given input text file. The program counts the unigrams and bigrams in the text and calculates the conditional probabilities of bigrams.

## Requirements
- mpi4py library
- Python 3
Usage
The program takes 3 arguments:

- --input_file : The input text file that will be analyzed.
- --merge_method : The method of merging the results of the workers. Two options are available: MASTER and WORKERS.
- --test_file : A test file that contains bigrams to calculate the conditional probability.

`mpiexec -n 4 python3 main.py --input_file input.txt --merge_method MASTER --test_file test.txt`
## Execution
When executed, the program divides the input text file into equal parts and assigns each part to a worker process. Each worker process counts the unigrams and bigrams in the assigned part and sends the results to the master process.

The master process then merges the results of the workers according to the chosen merge method. If the merge method is "MASTER", the master process receives the results from the workers and merges them. If the merge method is "WORKERS", the last worker process receives the results from the other workers and merges them before sending the final results to the master process.

The program then calculates the conditional probabilities of the bigrams in the test file using the merged results of the unigrams and bigrams.
