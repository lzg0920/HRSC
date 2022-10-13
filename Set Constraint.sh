#!/bin/bash
TYPE=$1
IDX=$2
BINARY=0
ITER_NUM=10
VEC_NUM=128
BELTA_ANT=0.1

#parameter setup
#synony
BELTA_SYN=0.6
ALPHA_SYN=0.025

TRAIN_PATH="../gen_data/drug/synonym_relation/output_2section_metapath.txt"
TRIPLET_PATH="../gen_data/drug/relation/GPS_relationgraph_new.txt"
SYNONYM_PATH="../gen_data/drug/synonym/drug_synonymgraph_new.txt"
ANTONYM_PATH="../gen_data/drug/antonym/null.txt"
VOCAB_PATH="../gen_data/drug/synonym_relation/volcubary.txt"

if [ $# -lt 1 ];then
	echo "Usage:./lrcwe_run.sh SAR 0"
	exit
fi

if [ $TYPE = "S" ];then
	echo "S training ..."
	MODEL_PATH="../gen_data/model/drug/synonym/drug_syn_emd_zhuyu_er${BELTA_SYN}"
	./lrcwe -train ${TRAIN_PATH} -synonym ${SYNONYM_PATH} -output ${MODEL_PATH} -save-vocab ${VOCAB_PATH} -belta-syn ${BELTA_SYN} -alpha-syn ${ALPHA_SYN} -size ${VEC_NUM} -window 7 -sample 1e-4 -negative 5 -hs 0 -binary ${BINARY} -cbow 0 -iter ${ITER_NUM}

         #MODEL_PATH="../gen_data/model/avg-lswe-cbow-${VEC_NUM}-model.s.${ITER_NUM}.${BELTA_SYN}.${ALPHA_SYN}.${IDX}.bin"
        #./lrcwe -train ${TRAIN_PATH} -synonym ${SYNONYM_PATH} -output ${MODEL_PATH} -save-vocab ${VOCAB_PATH} -belta-syn ${BELTA_SYN} -alpha-syn ${ALPHA_SYN} -size ${VEC_NUM} -window 7 -sample 1e-4 -negative 5 -hs 0 -binary ${BINARY} -cbow 1 -iter ${ITER_NUM}
	exit
else echo "Type error"
fi