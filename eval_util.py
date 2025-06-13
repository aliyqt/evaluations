"""
Code References:
BLUE/CIDER: https://github.com/Yale-LILY/SummEval
ROUGE: https://github.com/bheinzerling/pyrouge
       https://github.com/andersjo/pyrouge/tree/master/tools/ROUGE-1.5.5
"""
from summ_eval.bleu_metric import BleuMetric
from summ_eval.cider_metric import CiderMetric
import os
from pyrouge import Rouge155
import tempfile
import shutil
import nltk
nltk.download('punkt_tab')
import json
import re

""" ROUGE-1.5.5 """
def calculate_rouge_with_rouge155(candidates, references):
    # Create temporary directories for the ROUGE files
    temp_dir = tempfile.mkdtemp()
    try:
        # Create system and model directories
        system_dir = os.path.join(temp_dir, "system")
        model_dir = os.path.join(temp_dir, "model")
        os.makedirs(system_dir, exist_ok=True)
        os.makedirs(model_dir, exist_ok=True)

        # Write candidates and references to individual files
        for i, (candidate, reference) in enumerate(zip(candidates, references)):
            # File naming convention for ROUGE155
            with open(os.path.join(system_dir, f"cand.{i}.txt"), 'w', encoding='utf-8') as f:
                f.write(candidate.strip() + "\n")
            with open(os.path.join(model_dir, f"ref.{i}.txt"), 'w', encoding='utf-8') as f:
                f.write(reference.strip() + "\n")

        # Initialize ROUGE-155
        r = Rouge155()
        r.system_dir = system_dir
        r.model_dir = model_dir
        r.system_filename_pattern = 'cand.(\d+).txt'
        r.model_filename_pattern = 'ref.#ID#.txt'
        r.use_stemmer = True  # Optional, use stemmer for better matching

        # Run the ROUGE evaluation
        output = r.convert_and_evaluate()
        print("ROUGE scores:")
        print(output)
        scores = r.output_to_dict(output)

    finally:
        # Clean up temporary files
        shutil.rmtree(temp_dir)

    return output

""" BLEU+CIDEr+ROUGE """
def measure_metrics(gold_file_path, predictions_path):
    # Initialize the metrics
    bleu = BleuMetric()
    cider = CiderMetric(tokenize=True)

    # Read the reference and generated summaries
    label_set = []
    with open(predictions_path, 'r', encoding='utf-8') as f:
        for line in f:
            label_set.append(line.split(" | ")[0])
    with open(predictions_path, 'r', encoding='utf-8') as f:
        candidates = [line.split(" | ")[1].strip() for line in f.readlines()]
    # print(len(candidates), len(label_set), label_set[0])

    # Only keep matched references
    model, dataset, chart_type = predictions_path.split('/')[-1].split('_')
    chart_type = chart_type.split('.')[0]
    references,ori_references_ids = [],[]
    # print(gold_file_path)
    with open(gold_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            if item["id"] in label_set:
                references.append(item["caption"])
            if item["type"] == chart_type:
                ori_references_ids.append(item["id"])
            elif chart_type == "all":
                ori_references_ids.append(item["id"])

    print(f"Candidates obtained: {len(label_set)}, References_id matched: {len(references)}, References_tp matched: {len(ori_references_ids)}")
    if len(ori_references_ids) != len(label_set):
        print(f"Mismatch between number of references and candidates: {len(ori_references_ids)} != {len(label_set)}")
        # Determine the longer and shorter lists
        longer_list, shorter_list = (ori_references_ids, label_set) if len(ori_references_ids) > len(label_set) else (label_set, ori_references_ids)
        # Find elements in the longer list but not in the shorter one
        difference = [item for item in longer_list if item not in shorter_list]
        # print(difference)
    
    # use nltk to tokenize candidates and references
    # Tokenize the references and candidates
    references_t = [' '.join(nltk.tokenize.word_tokenize(ref)) for ref in references]
    candidates_t = [' '.join(nltk.tokenize.word_tokenize(cand)) for cand in candidates]
    # print(references)
    # Ensure the number of references and candidates match
    # assert len(references) == len(candidates), "Mismatch between number of references and candidates."
    if len(references) != len(candidates):
        print(f"Mismatch between number of references and candidates: {len(references)} != {len(candidates)}")
        return
    # Compute BLEU and CIDEr scores
    bleu_scores = bleu.evaluate_batch(candidates_t, references_t)
    cider_scores = cider.evaluate_batch(candidates, references)
    # Compute ROUGE-1.5.5 scores
    rouge_scores = calculate_rouge_with_rouge155(candidates, references)
    with open(model+"_"+chart_type+".txt", 'a') as f:
        f.write(f"Model: {model}, Dataset: {dataset}, ChartType: {chart_type}\n")
        f.write(f"References and Candidates: {len(ori_references_ids)} and {len(label_set)}\n")
        if len(ori_references_ids) != len(label_set):
            f.write(difference+"\n")
        f.write("BLEU:\n"+str(bleu_scores['bleu'])+"\n")
        f.write("CIDER:\n"+str(cider_scores['cider'])+"\n")
        f.write("ROUGE:\n"+rouge_scores+"\n\n")

    # Print the results
    print(f"BLEU Score: {bleu_scores['bleu']}")
    print(f"CIDEr Score: {cider_scores['cider']}")
    return bleu_scores['bleu'], cider_scores['cider']

""" Main Program """
results_dir = "results/"
files = [f for f in os.listdir(results_dir)]

for file in sorted(files):
    if file != '.DS_Store': # just check in MacOS
        model, dataset, chart_type = file.split('_')
        chart_type = chart_type.split('.')[0]
        print(f"->>> Model:{model}, Dataset:{dataset}, ChartType:{chart_type}")

        with open(model+"_"+chart_type+".txt", 'w') as f:
            f.write("")

        gold_file = "sorted_charts_output_pew_test.txt"
        print(f"->>> References:{gold_file}, Generated:{os.path.join(results_dir, file)}")
        try:
            bleu, cider = measure_metrics(gold_file, os.path.join(results_dir, file))
        except Exception as e:
            print(f"Error processing {file}: {e}")
            continue
