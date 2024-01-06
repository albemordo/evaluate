MODEL_PATH=$1


#python src/generate.py \
#    --data_folder data/ \
#    --model_folder mix \
#    --pretrained_model_name_or_path $MODEL_PATH \
#    --tokenizer_name_or_path meta-llama/Llama-2-7b-hf \
#    --num_return_sequences 40 \
#    --do_sample True \
#    --temperature 0.8 \
#    --prompt_template_path prompts/llama_2.txt


python src/generate.py \
    --data_folder data/ \
    --model_folder mix \
    --pretrained_model_name_or_path $MODEL_PATH \
    --tokenizer_name_or_path meta-llama/Llama-2-7b-hf \
    --prompt_template_path prompts/llama_2.txt