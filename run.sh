#!/bin/bash

echo "Starting $0 [$(date)]"

# do basic checks on arguments
# if [[ $# -eq 0 ]]; then
#         echo "No arguments provided, exiting..."
#         exit
# fi

# clear existing metadata
trash-put -r logs/ bookkeeping_projs/ files_stats/ files_tokens/ query_*.file blocks.file results.pair SCC_LOGS/

# tokenize input
# assuming zip input
python tokenizers/file-level/tokenizer.py zip
cat files_tokens/* > blocks.file
cp blocks.file clone-detector/input/dataset/

# run clone detector
cd clone-detector || exit
python controller.py

# gather results
cd ..
cat clone-detector/NODE_*/output8.0/query_* > results.pairs

echo "Finished SourcererCC [$(date)]"
