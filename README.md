# Name Entity Tagger
Using Max Entropy algorithm to predict the Name Entity Tag of the token in sentences  

Author: Yuanxu Wu  

## Prerequisites  
1. python 2.7.13  
2. java 1.8.0  

## How to compile and run  
1. get into the "code" folder in terminal (using cd code)  
2. javac -cp ".:maxent-3.0.0.jar:trove.jar" MEtrain.java  
3. javac -cp ".:maxent-3.0.0.jar:trove.jar" MEtag.java  
4. python FeatureBuilder.py <input filename> <output_filename>	// get train file advanced feature  
   for example, python FeatureBuilder.py input/CONLL_train.pos-chunk-name CONLL_train_ENHANCED_FEATURE.txt   
5. python FeatureBuilder.py <input filename> <output_filename>	// get test file advanced feature  
   for example, python FeatureBuilder.py input/CONLL_dev.pos-chunk CONLL_dev_test_ENHANCED_FEATURE.txt  
6. java -cp ".:maxent-3.0.0.jar:trove.jar" MEtrain <train advanced feature file> <output model name>  
   for example, java -cp ".:maxent-3.0.0.jar:trove.jar" MEtrain CONLL_train_ENHANCED_FEATURE.txt maxEntModel  
7. java -cp ".:maxent-3.0.0.jar:trove.jar" MEtag <test advanced feature file> <trained model name> <output tagged file name>  
   for example, java -cp ".:maxent-3.0.0.jar:trove.jar" MEtag CONLL_dev_test_ENHANCED_FEATURE.txt maxEntModel response.name  
8. python score.name.py   

## The outcome on development corpus  
50240 out of 51578 tags correct  
  accuracy: 97.41  
5917 groups in key  
6162 groups in response  
4957 correct groups  
  precision: 80.44  
  recall:    83.78  
  F1:        82.08  

## Local Features:  
1. case feature   
    The case feature contains initial case is upper or lower, all upper case or not, case sequence feature.  
2. tag feature  
    Tag feature contains the part-of-speech tag and BIO chunk tag.  
3. Token Information   
    These features are based on the token: such as contains digits, contains dollar sign, contains hyphen etc  
    and the length of the token.  
4. previous and next word feature  
    the features of previous token and next token.  
5. Zone feature  
    this token is in Head Line (HL), Author Line (AU), Date Line (DL), or text (TXT).  
6. Morphology feature  
    prefix and suffix features   
    and the maximum length of non-vowel characters in the token  
    and the shape of the token, for example, "Cccds" means Capital Char + lower case char + lower case char + number + symbol.  
7. Combined feature  
    Combine some feature together:  
    Combine the token is the first of a sentence or not, initial with capital or not, and Zone feature together.  
    Combine the token has all capital letter or not and Zone feature together.  
    Combine the token starts with a lower case letter and contains both upper and lower case letters, and Zone feature together.  
8. Bigram trigram feature  
    treat consecutive two words and consecutive three words as features.  
9. Rare word feature  
    The frequency of the token is under 3. Because this feature will take about 20mins to train and only get a very little improvement, so I removed it.  
10 Global features  
    I find a name list from https://pypi.python.org/pypi/human-names  
    and try to create a feature to check if the token is in this name set or not.  
    Because this feature will take about 20mins to train and also only get a very little improvement, so I removed it.  

Advanced Features: the final feature used in generate advanced feature txt  

    prev_init_case_F, curr_init_case_F, next_init_case_F, prev_tok_F, curr_tok_F, next_tok_F, prev_pos_F, curr_pos_F, next_pos_F, prev_all_upper_case_F, curr_all_upper_case_F, next_all_upper_case_F, curr_lower_case_F, curr_contain_hyphen_cap_F, curr_contain_upper_case_F, curr_contain_dot_F, curr_contain_quote_cap_F, curr_contain_number_F, curr_last_char_is_dot_F, curr_length, curr_max_consec_non_vowel_F, curr_first_init_cap_Zone_F, curr_all_caps_Zone_F, curr_mixed_caps_Zone_F, curr_sent_has_bracket_or_quotes_F, curr_suffix_3, curr_prefix_4, curr_bigram_F, trigram_F, cap_case_cap_F, Zone_F  

the other features I tried but didn't use in generating advanced feature are the features will generate negative improvement.  

## Tried Feature Set:  
prev_init_case_F : the initial case of the previous token  
curr_init_case_F : the initial case of current token  
next_init_case_F : the initial case of next token  
prev_tok_F : previous token  
curr_tok_F : current token  
next_tok_F : next token  
prev_pos_F : previous part-of-speech tag  
curr_pos_F : current part-of-speech tag  
next_pos_F : next part of speech tag  
prev_BIO_F : previous BIO chunk tag  
curr_BIO_F : current BIO chunk tag  
next_BIO_F : next BIO chunk tag  
prev_all_upper_case_F : the previous token is all uppercase or not  
curr_all_upper_case_F : current token is all uppercase or not  
next_all_upper_case_F : next token is all uppercase or not  
prev_contain_number_F : the previous token contain number or not  
curr_contain_number_F : current token contain number or not  
next_contain_number_F : next token contain number or not  
curr_lower_case_F : transit current token to lower case  
curr_contain_hyphen_cap_F : current token contain hyphen or not  
curr_contain_upper_case_F : current token contain uppercase or not  
curr_contain_dot_F : current token contain dot or not  
curr_contain_quote_cap_F : current token contain quote and capital letter or not  
curr_last_char_is_dot_F : last character is dot or not  
curr_length_F : the length of the current token  
curr_word_shape_F : the shape of the word, for example, "Cccds" means Capital Char + lower case char + lower case char + number + symbol  
curr_first_init_cap_Zone_F : this is a combined feature : current token is the first of a sentence or not, initial with capital or not, and Zone feature  
curr_all_caps_Zone_F : this is a combined feature : current token has all capital letter or not and Zone feature  
curr_mixed_caps_Zone_F : this is a combined feature : the token starts with a lower case letter, and contains  
both upper and lower case letters, and Zone feature  
curr_sent_has_bracket_or_quotes_F : the sentence contained this token has bracket or quotes or not  
Zone_F : this token is in Head Line (HL), Author Line (AU), Date Line (DL), or text (TXT)  
curr_prefix_2 : first two character  
curr_suffix_2 : last two character  
curr_prefix_3 : first three character  
curr_suffix_3 : last three character  
curr_prefix_4 : first four character  
curr_suffix_4 : last four character  
consecutive_three_tok_init_case_F : the initial case of three consecutive token   
curr_bigram_F : current word and next word  
prev_bigram_F : previous word and next word  
trigram_F : previous word and current word and next word  
cap_case_cap_F : case sequence  
curr_max_consec_non_vowel_F : the maximum length of non-vowel characters in the current token  
