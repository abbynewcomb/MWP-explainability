import pandas as pd
import nltk
from torch.utils.data import DataLoader

from src.modelv2 import run_validation, Seq2SeqModel
from src.dataloader import TextDataset
from src.utils.sentence_processing import sents_to_idx, process_batch


def input_reduction(config, model, dataloader, voc1, voc2, device, logger, epoch_num, beam_size=5):
    """
    function to perform input reduction. evaluates model on 
        successively smaller inputs of same question until 
        it reaches the smallest possible input that still gives 
        the correct answer. config.mode should already be 
        set to input_reduction
    input:
        single question and equation
    output:
        pandas.DataFrame of gradually reduced input and confidence scores for each
    """
    
    gradual_reduced_input_list = pd.DataFrame({
        "Question": [],
        "Removed Word": [],
        "Model Confidence": [],
        "Generated Equation": [],
        "Score": [],
    })

    # get prediction and conf score for original question, add to result df
    val_res = run_validation(
        config, model, dataloader, voc1, voc2, device, logger, epoch_num
    )
    gradual_reduced_input_list = gradual_reduced_input_list.append({
        "Question": val_res.at[0,"Question"],
        "Removed Word": None, # is original question, nothing removed yet
        "Model Confidence": val_res.at[0,"Model Confidence"],
        "Generated Equation": val_res.at[0,"Generated Equation"],
        "Score": val_res.at[0,"Score"],
    }, ignore_index=True)
    
    # check that answer to initial question is correct
    if val_res.at[0,"Score"] == 1:
        logger.info("Beginning input reduction algorithm")
        logger.info("Orig Model Confidence: {}\tOrig Question: {}".format(
            gradual_reduced_input_list.at[ 0, "Model Confidence" ],
            gradual_reduced_input_list.at[ 0, "Question" ])
        )
        
        # grab answer and numbers from val_res
        numbers = val_res.at[0,"Numbers"]
        answer = val_res.at[0, "Answer"]
        eqn = val_res.at[0, "Actual Equation"]
        
        keep_going = True # we keep going until the reduced input w/ highest conf is not correct

        while keep_going:

            # remove least important token, append info to reduced input list
            res_dict = remove_one_token(
                config = config,
                model = model,
                voc1 = voc1,
                voc2 = voc2,
                device = device,
                logger = logger,
                epoch_num = epoch_num,
                instance = gradual_reduced_input_list.at[ len(gradual_reduced_input_list)-1, "Question" ],
                numbers = numbers,
                answer = answer,
                eqn = eqn,
                beam_size = beam_size,
            )
            if not any(res_dict): # no options to reduce (only necessary tokens remaining)
                break
            gradual_reduced_input_list = gradual_reduced_input_list.append({
                "Question": res_dict["q"],
                "Removed Word": which_word_removed(
                    gradual_reduced_input_list.at[ len(gradual_reduced_input_list)-1, "Question"],
                    res_dict["q"],
                ),
                "Model Confidence": res_dict["conf"],
                "Generated Equation": res_dict["gen_eq"],
                "Score": res_dict["score"],
            }, ignore_index=True)
            
            print("Model Confidence: {}\tQuestion: {}".format(
                res_dict["conf"],
                res_dict["q"],
            ), flush=True)
            
            # check if answer is correct. if not, stop looping
            if gradual_reduced_input_list.at[ len(gradual_reduced_input_list)-1, "Score" ] == 0:
                keep_going = False

    else: # model prediction for first question was incorrect
        logger.info("incorrect prediction from model for original question")
                
    # return result dataframe
    return gradual_reduced_input_list


def remove_one_token(config, model, voc1, voc2, device, logger, epoch_num, instance, numbers, answer, eqn, beam_size):
    """
    compute best input which is one smaller than previous.

    notable input: instance, the current thing to be made smaller
                   beam_size, the size of the beam

    output: dict of necessary info {q, gen_eq, score, conf}
    """
    # format instance with other required columns (equation, numbers, answer) and load to dataloader
    instance = pd.DataFrame({
        "Question": [instance],
        "Equation": [eqn],
        "Numbers": [numbers],
        "Answer": [answer],
    })
    dataset = TextDataset(
        data_path=None,
        dataset=config.dataset,
        datatype="test",
        dataframe=instance, # the important line
        max_length=config.max_length,
        is_debug=config.debug,
        mode=config.mode,
    )
    dataloader = DataLoader(
        dataset, batch_size=config.batch_size, shuffle=False, num_workers=5
    )


    for idx, layer in enumerate(model.modules()):
        if idx < 2:
            print("{} {}".format(idx, layer))
    
    # start of using gradients                                                                      
    for data in dataloader:
        ques = ["rainbow"]
        
        sent1s = sents_to_idx(voc1, ques, config.max_length)
        sent2s = sents_to_idx(voc2, data['eqn'], config.max_length)
        sent1_var, sent2_var, input_len1, input_len2  = process_batch(sent1s, sent2s, voc1, voc2, device)

        model.get_gradients(config, ques, sent1_var, sent2_var, input_len1, input_len2, device, logger)
    
           
    return pd.DataFrame([])



def remove_each_word(question):
    """
    creates a list of perturbed questions with each possible word removed
    """
    res = [] # list of questions with word removed
    tokens = nltk.word_tokenize(question)
    for token in tokens:
        if not (token[:6] == "number"):
            res.append(' '.join(word for word in tokens if word != token))
    return res


def which_word_removed(q1, q2):
    """
    inputs:
        q1 a question
        q2 a question with one fewer word
    output:
        the word that exists in q1 but not q2
    """
    q1_tokens = nltk.word_tokenize(q1)
    q2_tokens = nltk.word_tokenize(q2)

    for i in range(len(q2_tokens)):
        if not q1_tokens[i] == q2_tokens[i]:
            return q1_tokens[i]
        elif i == (len(q2_tokens))-1: # in case last word is the uncommon one, to avoid bad index on q2
            return q1_tokens[ i+1 ]

