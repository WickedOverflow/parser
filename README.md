[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
# Technical Challenge
## Description

This repo contains my solutions to the given technical challenges. I did not start a timer, but I think it took about two hours from start to complete finish including writing this README and uploading the project. Gentlemen, I am currently writing this from the passenger seat of a car on a clean laptop tethered to my phone over Memorial Day weekend, so I demand repercussions for my pain in the form of food and stouts if I come aboard.

After taking a look at the log and the questions to be answered, I did what I usually do: check if someone has already written a tool to make my life easy. It turns out that there are a few incomplete or basic [responder parsers](https://github.com/Mili-NT/ResponderParser "responder parsers"), but nothing I think that would help me answer all of the questions.

For the first question, I started Notepad++. Ctrl-f, enter each protocol, click "Count", and record them. 
![N++](https://user-images.githubusercontent.com/106585708/171133585-eeaff096-f7d6-44fb-b287-36b597962364.PNG)

At this moment a decision had to be made. Do I:

1. Cheese my way through this with existing tools and Ctrl-f?

2. Fumble with bash scripts and regular expressions?

3. Code something in Python?

It dawned on me at that moment that sure, I could probably cheese my way through and I might would do that in the real world if I needed an answer fast, but I think the point is that I need to display a little programming ability. Not to mention that I did not have a Linux image or full set of developer tools on this machine during my trip. However, I did have a base installation of Python 3 and do not get to program as often as I would like, so that is what I did.

The code is straight forward and I will explain a little about my approach under each task. **Note**, I did not include any snippets of hashes here just because this repo is public and we are all known entities. Running the code against the provided log file will produce all of the relevant results though.


## Task #1: Of all the `Poisoned` responses logged, how many queries of each MNR protocol were sent during the time Responder was running?

- MDNS total: 7162 
- LLMNR total: 6579 
- NBT-NS total: 477

For this task all I did was open the log file, read each line, and checked if any of the three protocols existed in the line. If so, increment a counter for the one that did. These values are printed at the end. Using the results from Notepad++, I can confirm that the results are accurate.


## Task 2: Of the `Poisoned` responses logged, what are the 10 most common hosts (i.e. hashes of the hostname)?

Most common hosts | Number of times seen
------------------|---------------------
..... | 5705
..... | 3647
..... | 1048
..... | 490
..... | 396
..... | 382
..... | 319
..... | 190
..... | 188
..... | 181

Again, the hashes are redacted here, but present in the results. I do need to review regular expressions, but I used a basic one here to split each line using the `re` library. That allowed me to easily have an index directly to the hash. From there, I check if I have that hash in a dictionary. If I do, I increment its value by one. If not, I store it as a key in the dictionary with a value of one. Once all lines have been examined, the dictionary contains every host hash and the amount of times it was seen in the log file. The dictionary is then converted to a `Counter` so that the builtin `most_common()` function could be used to find the top 10 host hashes.


## Task 3: Of the `Poisoned` responses logged, what are the 10 most common queries?

Most common queries | Number of times seen
--------------------|---------------------
..... | 3672
..... | 1836
..... | 1184
..... | 1132
..... | 1057
..... | 855
..... | 656
..... | 655
..... | 623
..... | 619

Very similar to Task 2, but the regular expression is slightly different so that the other hash in each entry could have an index.


## Task 4: A NTLM version 1 hash was leaked to Responder. What is the `Client` that sent those credentials? How many times was a `Poisoned` response sent to that host?

Client: .....

Number of poisoned responses sent: 11

This one is a little cheesy, but it works by searching each line for the string "NTLM". If it finds it, it then looks for the string "Client: " in the line. Once that is found, the string is split so that client hash can be saved. I then opened the logfile again, searching each line specifically for the client has **and** the string "Poisoned" because some of the log entries specify that Responder skipped previously captured hashes and we would match on those strings without the additional check. Each one of those that are found increment a counter, and it is printed with the client hash at the end of the log file. 


## Task 5: When was Responder started? When did it end?
Start: 2020-12-14 13:41:27

End: 2020-12-15 14:07:53

Dates and times are nortorious for being the bane of a programmer's existence, but these seem tame and thankfully Python has the `datetime` module. Each line of the log is split at the '-' to get an index to the timestamp information. Each timestamp is appended as a datetime object (by specifying the format to the `strptime()` function). Once all entries have been added, the builtin `min()` and `max()` functions are used to find the start (lowest time in log) and end (highest time in log) times, respectively.

## Notes

- Solutions were crafted around this specific log file. I do not claim (and would expect) crashes on anything else. For example, I made some guesses about the format of the timestamps based on the information I have. They may or may not be wrong, but they work for the slice of logs given.

- I left several print statements in the code that I made use of to verify the data. They are commented out, but you can uncomment them for more verbosity.

- There is no error handling.

- There are no test cases.

- The log file is hardcoded as "responder.log".

- The program does not accept any arguments.

- I did lint the code for PEP 8, but it is not perfect.

- I did not comment the code because I left the comments here.

I hope this is to everyone's satisfaction and I hope to hear from you soon.
