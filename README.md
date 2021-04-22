# Jobcoin-Mixer
![jobcoin_diag](https://user-images.githubusercontent.com/82118903/115753675-74b75e80-a369-11eb-82f6-1cc68dd9af8b.png)

# Enhancements/Implementation Concepts
1. Jobcoin-mixer API in the event we want to host this service
	* Primary opsec benefits
		* All jobcoin p2p actions don't originate from users network
		* Mixing logic not running on user host/don't have to ship jobcoin-mixer business logic
2. In practice implementing timing delays and jitter rates between mixing actions will enhance privacy (make tracing more challenging)
3. Depending on the level of activity on the p2p network it might make sense to be able to generate decoy transactions
4. If this is shipping as mixing self-service software, may want to examine the JA3 JA3S fingerprint for client networking opsec
5. Further stress testing/edge case analysis on the jobcoin p2p network will help define exception handling requirements/enhancements
6. More cleanup after distribution accounts complete their work  
