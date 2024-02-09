.PHONY: clear

clear:
	-rm -r logs/ bookkeeping_projs/ files_stats/ 			\
	file_block_stats/ blocks_tokens/ files_tokens/ 	  \
	query_1.file blocks.file results.pair SCC_LOGS/ 	\
	output/*
