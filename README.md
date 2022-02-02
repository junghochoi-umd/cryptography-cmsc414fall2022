## General Description

In this project, you will be attacking a weak ciphersuite in an online
bank. The bank is using a secure **128-bit block cipher**, with a
*unique key* per session. To make a streaming cipher from this, the
bank is using the cipher in ECB mode.

As an attacker, you were able to inspect the ciphertext stream sent by
you to the bank's server. Due to some technical limitations, you were
unable to capture the server's responses, and you were only able to do
this once.  However, you know exactly what operations you performed,
and in what order, so you should be able to figure out the encrypted
message formats, despite *not knowing the plaintext format*. That is,
the *only* things you have are what you entered into the bank's
website, and the corresponding ciphertext stream.

From this, you will need to do the following:

 * Learn the format of the messages
 * Write a program to parse these messages and generate new messages
 * Perform a number of passive- and active-wiretapping attacks on
   the session of *another* customer (the target), which uses a
   *different* key


## The Reference Stream

The file `reference.out` contains the following sequence of requests, in the
order given:

 1. A balance request for your checking account
 2. A $100 transfer from your checking account to your savings
    account, to be executed immediately
 3. A balance request for your checking account
 4. A balance request for your savings account
 5. A $1000 transfer from your savings account to your checking
    account, to be executed immediately
 6. A $1000 transfer from your savings account to your checking
    account, to be executed tomorrow
 7. A balance request for your savings account
 8. A request for payment of $1000 to your checking account from your
    savings account
 9. A balance request for your checking account



## Tasks

There are four tasks, and each will require a separate executable.
For instance, the executable for task 1 will be named `task1`.  Note,
this should ***not*** be `task1.x`, `task1.exe`, `task1.sh`,
`task1.py`, or any other file extension.  If this executable must be
compiled, you must provide a `Makefile` to do the compilation, which
will be called *without arguments*. That is, do not expect us to run
`make task1`.

Each task will operate on a *separate session*. That is, they will all
be encrypted with different keys. You will have limited information
about each session.

See the Implementation Notes below for formatting of output and other
requirements.

### Task 1

For this task, you will provide an executable named `task1` that reads
the ciphertext for a session and outputs

 * The types of messages, in order, with each on a separate line

The ciphertext will be provided as the only command-line argument to
your executable, and will be in the same format as the reference
stream.

### Task 2

For this task, you will provide an executable named `task2` that reads
the ciphertext for a session and outputs

 * The types of messages, in order, with each on a separate line
 * A replay of a message that transfers money into your account,
   written to a file named `task2.out`

For this session, you know that *exactly one* message includes your
account. The file `task2.out` should include the **entire** stream,
with your replay added to it. That is, there should be exactly one
more message in `task2.out` than the input stream.

As before, the input ciphertext stream will be provided as the only
command-line argument to your executable, and will be in the same
format as other streams.

### Task 3

For this task, you will provide an executable named `task3` that reads
the ciphertext for a session and outputs

 * The types of messages, in order, with each on a separate line
 * A modified money transfer to your account, where the amount in the
   transfer is changed to a valid new value, written to a file
   `task3.out`

For this session, you know that the target sent a money transfer
request to your account for $10, and requested payments from at least
one other account. No other requests involving your account are in
this session.

Your executable should produce a file `task3.out` containing the input
ciphertext with the modified message. That is, `task3.out` should
contain the same messages as the input, but with the amount changed in
the payment to your account.

As before, the input ciphertext stream will be provided as the only
command-line argument to your executable, and will be in the same
format as other streams.

### Task 4

For this task, you will provide an executable named `task4` that reads
the ciphertext for a session and outputs

 * The types of messages, in order, with each on a separate line
 * A money transfer to your account *instead of* a payment request
   from your account, written to a file `task4.out`

For this session, you know that the target requested payment from your
account, and this is the only request involving your account. You must
convert this payment request *from* your account into a money transfer
*to* your account.

Your executable should produce a file `task4.out` containing the input
ciphertext with the modified message. That is, `task4.out` should
contain the same messages as the input, but with the request for
payment from you changed to a transfer to you.

As before, the input ciphertext stream will be provided as the only
command-line argument to your executable, and will be in the same
format as other streams.

## Implementation Notes

The required output must match what we have asked for **exactly**.
Anything not part of the required output should be printed to standard
error, not standard output.

The following table shows the expected way to print message types:

| **Message Type**    | **Value to Print** |
| ------------------- | ------------------ |
| balance request     | BALANCE            |
| money transfer      | TRANSFER           |
| request for payment | INVOICE            |


## Submission

You must commit your submission to git by the deadline. Pushes to
gitlab after the deadline are acceptable, but late commits will only
be accepted if you were granted an extension.

Do not add compiled files to git, only scripts, source code, and (if
needed) a `Makefile`.

## Scoring

 * Identifying all messages correctly will cumulatively be worth 20
   points (tasks 1-4)
 * Producing valid messages will cumulatively be worth 15 points
   (tasks 2-4)
 * Correctly modifying a messages will cumulatively be worth 10 points
   (tasks 3 and 4)
 * Correctly changing the type of a message will be worth 5 points
   (task 4)

## Tips

 * While you must provide four separate executables, you will probably
   want to have some code in common between them. This might be an
   additional `.c` and `.h` file, a python file to import, or
   something else. You might even have a single binary, and bash
   scripts to call it with appropriate arguments for the individual
   tasks.
