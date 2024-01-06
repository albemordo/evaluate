MODEL_PATH=$1


python src/generate.py \
    --data_folder data/ \
    --model_folder mix \
    --pretrained_model_name_or_path $MODEL_PATH \
    --tokenizer_name_or_path meta-llama/Llama-2-7b-hf \
    --num_return_sequences 40 \
    --num_beams 10 \
    --prompt_template_path prompts/llama_2.txt