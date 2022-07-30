import pandas as pd
import nltk
from torch.utils.data import DataLoader

from src.modelv2 import run_validation
from src.dataloader import TextDataset


def input_reduction(config, model, dataloader, voc1, voc2, device, logger, epoch_num):
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
        "Actual Equation": [],
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
            
            # get list of options for removing each word in previous level question
            options = remove_each_word(
                gradual_reduced_input_list.at[ len(gradual_reduced_input_list)-1, "Question" ]
            )
            if len(options) == 0:
                break;
            # format options with other required columns (equation, numbers, answer)
            options = pd.DataFrame({
                "Question": options,
                "Equation": [eqn] * len(options),
                "Numbers": [numbers] * len(options),
                "Answer": [answer] * len(options),
            })

            
            # load data into dataloader object
            dataset = TextDataset(
                data_path=None,
                dataset=config.dataset,
                datatype="test",
                dataframe=options, # the important line
                max_length=config.max_length,
                is_debug=config.debug,
                mode=config.mode,
            )
            dataloader = DataLoader(
                dataset, batch_size=config.batch_size, shuffle=False, num_workers=5
            )

            
            # make predictions and get confidence scores and actual scores for reduced inputs
            val_res = run_validation(
                config, model, dataloader, voc1, voc2, device, logger, epoch_num

            )
            if len(gradual_reduced_input_list) == 1:
                print(val_res[["Question","Model Confidence"]])
            # grab question with highest conf score, save to gradual_reduced_input_list
            val_res["Model Confidence"] = pd.to_numeric(val_res["Model Confidence"])
            highest_conf_index = val_res["Model Confidence"].idxmax()
            print("Model Confidence: {}\tQuestion: {}".format(
                val_res.at[ highest_conf_index, "Model Confidence" ],
                val_res.at[ highest_conf_index, "Question" ]
            ), flush=True)
            gradual_reduced_input_list = gradual_reduced_input_list.append({
                "Question": val_res.at[highest_conf_index,"Question"],
                "Removed Word": which_word_removed(
                    gradual_reduced_input_list.at[ len(gradual_reduced_input_list)-1, "Question" ],
                    val_res.at[ highest_conf_index, "Question" ],
                ),
                "Model Confidence": val_res.at[highest_conf_index,"Model Confidence"],
                "Actual Equation": val_res.at[highest_conf_index, "Actual Equation"],
                "Generated Equation": val_res.at[highest_conf_index,"Generated Equation"],
                "Score": val_res.at[highest_conf_index,"Score"],
            }, ignore_index=True)
            
            
            # check if answer is correct. if not, stop looping
            if gradual_reduced_input_list.at[ len(gradual_reduced_input_list)-1, "Score" ] == 0:
                keep_going = False

    else: # model prediction for first question was incorrect
        logger.info("incorrect prediction from model for normal question")
                
    # return result dataframe
    return gradual_reduced_input_list


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
