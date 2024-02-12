#!/bin/bash

echo "Starting $0 [$(date)]"

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
cat clone-detector/NODE_*/output*.0/query_* > results.pairs

echo "Finished SourcererCC [$(date)]"
