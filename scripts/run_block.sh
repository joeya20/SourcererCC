#!/bin/bash

echo "Starting $0 [$(date)]"

# do basic checks on arguments
# if [[ $# -eq 0 ]]; then
#         echo "No arguments provided, exiting..."
#         exit
# fi

# clear existing metadata
trash-put -r logs/ file_block_stats/ blocks_tokens/ bookkeeping_projs/ results.pairs blocks.file

# tokenize input
# assuming zip input
python tokenizers/block-level/tokenizer.py zipblocks
cat blocks_tokens/* > blocks.file
cp blocks.file clone-detector/input/dataset/

# run clone detector
cd clone-detector || exit
python controller.py

# gather results
cd ..
cat clone-detector/NODE_*/output8.0/query_* > results.pairs

echo "Finished SourcererCC [$(date)]"
