# Jobcoin-Mixer

## Getting Started

```
  $ mkdir jobcoin-mixer

  $ cd jobcoin-mixer

  $ virtualenv venv
  created virtual environment CPython3.8.5.final.0-64 in 206ms
  [...]

  $ source venv/bin/activate
  (venv) user@host:

  $ git clone https://github.com/supercerealized/jobcoin-mixer.git

  Cloning into 'jobcoin-mixer'...
  remote: Enumerating objects: 107, done.
  remote: Counting objects: 100% (107/107), done.
  remote: Compressing objects: 100% (73/73), done.
  remote: Total 107 (delta 66), reused 67 (delta 30), pack-reused 0
  Receiving objects: 100% (107/107), 253.44 KiB | 2.03 MiB/s, done.
  Resolving deltas: 100% (66/66), done.

  $ pip3 install -r requirements.txt
  $ python3 cli.py 
    Welcome to the Jobcoin mixer!

```

## Process Flowchart
![jobcoin_diag](https://user-images.githubusercontent.com/82118903/115753675-74b75e80-a369-11eb-82f6-1cc68dd9af8b.png)

## Enhancements/Implementation Concepts
1. Jobcoin-mixer API in the event we want to host this service
	* Primary opsec benefits
		* All jobcoin p2p actions don't originate from users network
		* Mixing logic not running on user host/don't have to ship jobcoin-mixer business logic
	* Defining api endpoints with Flask to jobcoin functionality is a simple api resource mapping exercise. Given more time, shipping a sever package might make sense
		* Server validation may involve hadling cross-origin and ItsDangerous style callback 
2. In practice implementing timing delays and jitter rates between mixing actions will enhance privacy (make tracing more challenging)
3. Depending on the level of activity on the p2p network it might make sense to be able to generate decoy transactions
4. If this is shipping as mixing self-service software, may want to examine the JA3 JA3S fingerprint for client networking opsec
5. Further stress testing/edge case analysis on the jobcoin p2p network will help define exception handling requirements/enhancements
6. More cleanup after distribution accounts complete their work  
7. Currently verbose by design for assessment -- can use logging library with flags for verbose/DEBUG implementation.
	* verbosity should be assessed against privacy constraints when implemented (see 1.).
	* even when implemented as a hosted service there may be an expectation or preference for a zero log policy
