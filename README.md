# Information Retrieval

# Goal

In this programming assignment, you will build a simple indexing and retrieval system.
For the assignment, use the stories dataset available at http://archives.textfiles.com/stories.zip.
Write your code in C++, Java, or Python.
Specifically, it involves the following tasks:
1. Build a uni-gram inverted index over terms of the dataset.
   - Preprocess documents in the dataset to remove punctuations and numbers, perform stemming and normalization and so on.
   - Find and use a suitable stemming library while generating terms.
   - Use the SPIMI-Invert algorithm. But, assume that free memory is enough to keep a whole index as well as the dataset. That is, you don't need to write the index and dictionary to disk.
2. Implement Boolean retrieval for the following queries.
   - X OR Y
   - X AND Y
   - X AND NOT Y
   - X OR NOT Y
3. Implement ranked retrieval using tf-idf scoring that supports free text queries.
   - Implement both TAAT and DAAT
4. Write up a report describing your program and results.
   - Describe your program. Do not include the source code in the report.
   - Report statistics of the index.
   - Carefully select a few sample Boolean queries not to produce too many results.
   - Describe whatever you think is meaningful. For ranked retrieval, include the comparison between TAAT and DAAT.
The due date is 19st June 2022.



Please submit the source code and report as follows.
- Zip the source code into a single file and name it using your student id (e.g., 202200000.zip).
- Submit the report as a separate file in pdf format.