import re
import sys

class Feature_Vector:
	prev_init_case_F = "prev_init_case="
	curr_init_case_F = "curr_init_case="
	next_init_case_F = "next_init_case="
	prev_tok_F = "prev_tok="
	curr_tok_F = "curr_tok="
	next_tok_F = "next_tok="
	prev_pos_F = "prev_pos="
	curr_pos_F = "curr_pos="
	next_pos_F = "next_pos="
	prev_all_upper_case_F = "prev_all_upper_case="
	curr_all_upper_case_F = "curr_all_upper_case="
	next_all_upper_case_F = "next_all_upper_case="
	prev_contain_number_F = "prev_contain_number_F="
	curr_contain_number_F = "curr_contain_number_F="
	next_contain_number_F = "next_contain_number_F="
	Zone_F = "Zone="

	curr_lower_case_F = ""
	curr_contain_hyphen_cap_F = ""
	curr_contain_upper_case_F = ""
	curr_contain_dot_F = ""
	curr_contain_quote_cap_F = ""
	curr_last_char_is_dot_F = ""
	curr_length = ""
	curr_word_shape_F = ""

	curr_first_init_cap_Zone_F = "" 
	curr_all_caps_Zone_F = ""
	curr_mixed_caps_Zone_F = ""

	sent_start_flag = 0

	curr_sent_has_bracket_or_quotes_F = "curr_sent_has_bracket_or_quotes=0"

	curr_prefix_1 = ""
	curr_suffix_1 = ""
	curr_prefix_2 = ""
	curr_suffix_2 = ""
	curr_prefix_3 = ""
	curr_suffix_3 = ""
	curr_prefix_4 = ""
	curr_suffix_4 = ""

	consecutive_three_tok_init_case_F = ""

	curr_bigram_F = "curr_bigram="	## curr_tok + next_token
	prev_bigram_F = "prev_bigram="

	prev_t = ""
	next_t = ""

	trigram_F = "trigram="
	cap_case_cap_F = "cap_case_cap="

	curr_max_consec_non_vowel_F = ""

	prev_NE_tag_F = "prev_NE_tag="

	##rare_word_F = ""

	##in_name_set_F = ""

	def __init__(self, tok, pos, bio, ne):
		self.Token = tok
		self.POS = pos
		self.BIO = bio
		self.NE = ne

def generate_curr_feature(Docts):
##	word_list = []
##	for doc in Docts:
##		for sent in doc:
##			for fv in sent:
##				word_list.append(fv.Token.lower())

	for doc in Docts:
		for sent in doc:
			for fv in sent:
				fv.curr_pos_F = "curr_pos="+fv.POS
				fv.curr_tok_F = "curr_tok="+fv.Token
				fv.curr_length = "curr_length="+str(len(fv.Token))
				if fv.Token[0].isupper():
					fv.curr_init_case_F = "curr_init_case=upper"
				else:
					fv.curr_init_case_F = "curr_init_case=lower"
				if fv.Token.isupper():
					fv.curr_all_upper_case_F = "curr_all_upper_case=1"
				else:
					fv.curr_all_upper_case_F = "curr_all_upper_case=0"
				fv.curr_lower_case_F = fv.Token.lower()
				if "-" in fv.Token and any(i.isupper() for i in fv.Token):
					fv.curr_contain_hyphen_cap_F = "curr_contain_hyphen_cap=1"
				else:
					fv.curr_contain_hyphen_cap_F = "curr_contain_hyphen_cap=0"
				if "." in fv.Token:
					fv.curr_contain_dot_F = "curr_contain_dot=1"
				else:
					fv.curr_contain_dot_F = "curr_contain_dot=0"
				flag_contain_upper = 0
				for i in range(len(fv.Token)):
					if i > 1 and fv.Token[i].isupper():
						flag_contain_upper = 1
						fv.curr_contain_upper_case_F = "curr_contain_upper=1"
				if flag_contain_upper == 0:
					fv.curr_contain_upper_case_F = "curr_contain_upper=0"
				if "\'" in fv.Token and any(i.isupper() for i in fv.Token):
					fv.curr_contain_quote_cap_F = "curr_contain_quote_cap=1"
				else:
					fv.curr_contain_quote_cap_F = "curr_contain_quote_cap=0"
				if any(i.isdigit() for i in fv.Token):
					fv.curr_contain_number_F = "curr_contain_number=1"
				else:
					fv.curr_contain_number_F = "curr_contain_number=0"
				if fv.Token.endswith("."):
					fv.curr_last_char_is_dot_F = "curr_last_char_is_dot=1"
				else:
					fv.curr_last_char_is_dot_F = "curr_last_char_is_dot=0"

				if len(fv.Token) > 4:
					fv.curr_prefix_4 = "prefix="+fv.Token[:4]
				else:
					fv.curr_prefix_4 = "prefix="+fv.Token
				if len(fv.Token) > 3:
					fv.curr_prefix_3 = "prefix="+fv.Token[:3]
				else:
					fv.curr_prefix_3 = "prefix="+fv.Token
				if len(fv.Token) > 2:
					fv.curr_prefix_2 = "prefix="+fv.Token[:2]
				else:
					fv.curr_prefix_2 = "prefix="+fv.Token
				
				if len(fv.Token) > 4:
					fv.curr_suffix_4 = "suffix="+fv.Token[-4:]
				else:
					fv.curr_suffix_4 = "suffix="+fv.Token
				if len(fv.Token) > 3:
					fv.curr_suffix_3 = "suffix="+fv.Token[-3:]
				else:
					fv.curr_suffix_3 = "suffix="+fv.Token
				if len(fv.Token) > 2:
					fv.curr_suffix_2 = "suffix="+fv.Token[-2:]
				else:
					fv.curr_suffix_2 = "suffix="+fv.Token
				for i in fv.Token:
					if i.isupper():
						if i == 'A' or i == 'E'or i == 'I'or i == 'O'or i == 'U':
							fv.curr_word_shape_F = fv.curr_word_shape_F+"A"	## capital character
						else:
							fv.curr_word_shape_F = fv.curr_word_shape_F+"B"
					elif i.islower():
						if i =='a' or i =='e'or i =='i'or i =='o'or i =='u':
							fv.curr_word_shape_F = fv.curr_word_shape_F+"a"	## lower case character
						else:
							fv.curr_word_shape_F = fv.curr_word_shape_F+"b"
					elif i.isdigit():
						fv.curr_word_shape_F = fv.curr_word_shape_F+"d"	## number
					else:
						fv.curr_word_shape_F = fv.curr_word_shape_F+"s"	## symbol
				fv.curr_word_shape_F = "curr_word_shape="+fv.curr_word_shape_F

				max_consec_non_vowel = 0
				consec_non_vowel = 0
				vowel_set = set()
				vowel_set.add("A")
				vowel_set.add("E")
				vowel_set.add("I")
				vowel_set.add("O")
				vowel_set.add("U")
				vowel_set.add("a")
				vowel_set.add("e")
				vowel_set.add("i")
				vowel_set.add("o")
				vowel_set.add("u")				
				for i in fv.Token:
					if i not in vowel_set:
						consec_non_vowel = consec_non_vowel+1
					else:
						if consec_non_vowel > max_consec_non_vowel:
							max_consec_non_vowel = consec_non_vowel
				fv.curr_max_consec_non_vowel_F = "curr_max_consec_non_vowel="+str(max_consec_non_vowel)
				##if word_list.count(fv.Token.lower()) < 3:
				##	print(fv.Token)
				##	fv.rare_word_F = "rare_word=1"
				##else:
				##	fv.rare_word_F = "rare_word=0"
				##name_set = set()
				##get_name_set_from_additional(name_set)
				##if fv.Token in name_set:
				##	print(fv.Token)
				##	fv.in_name_set_F = "in_name_set=1"
				##else:
				##	fv.in_name_set_F = "in_name_set=0"

	generate_combined_feature(Docts)

def generate_prev_next_feature(Docts):
	## previous feature
	prev_tok = "prev_tok="
	prev_pos = "prev_pos="
	prev_init_case = "prev_init_case="
	prev_all_upper_case = "prev_all_upper_case="
	prev_contain_number = "prev_contain_number_F="
	prev_NE_tag = "prev_NE_tag="
	prev_t = ""
	for doc in Docts:
		for sent in doc:
			for fv in sent:
				fv.prev_tok_F = prev_tok
				prev_tok = "prev_tok="+fv.Token
				fv.prev_pos_F = prev_pos
				prev_pos = "prev_pos="+fv.POS
				fv.prev_NE_tag_F = prev_NE_tag
				prev_NE_tag = " prev_NE_tag="+fv.NE
				fv.prev_init_case_F = prev_init_case
				prev_init_case = "prev_"+fv.curr_init_case_F
				fv.prev_all_upper_case_F = prev_all_upper_case
				prev_all_upper_case = "prev_"+fv.curr_all_upper_case_F
				fv.prev_contain_number_F = prev_contain_number
				prev_contain_number == "prev_"+fv.curr_contain_number_F
				fv.prev_bigram_F = "prev_bigram="+prev_t+"_"+fv.Token
				fv.prev_t = prev_t
				prev_t = fv.Token

	
	## next feature
	next_tok = "next_tok="
	next_pos = "next_pos="
	next_init_case = "next_init_case="
	next_all_upper_case = "next_all_upper_case="
	next_contain_number = "next_contain_number="
	next_t = ""
	for doc in Docts[::-1]:
		for sent in doc[::-1]:
			for fv in sent[::-1]:
				fv.next_tok_F = next_tok
				next_tok = "next_tok="+fv.Token
				fv.next_pos_F = next_pos
				next_pos = "next_pos="+fv.POS
				fv.next_init_case_F = next_init_case
				next_init_case = "next_"+fv.curr_init_case_F
				fv.next_all_upper_case_F = next_all_upper_case
				next_all_upper_case = "next_"+fv.curr_all_upper_case_F
				fv.next_contain_number_F = "next_"+fv.curr_contain_number_F
				fv.curr_bigram_F = "curr_bigram="+fv.Token+"_"+next_t
				fv.next_t = next_t
				next_t = fv.Token

	generate_trigram_feature(Docts)

	## prev curr next consecutive three token inital case feature
	for doc in Docts:
		for sent in doc:
			for fv in sent:
				curr_ic = ""
				next_ic = ""
				prev_ic = ""
				if "1" in fv.curr_init_case_F:
					curr_ic = "1"
				else:
					curr_ic = "0"
				if "1" in fv.prev_init_case_F:
					prev_ic = "1"
				else:
					prev_ic = "0"
				if "1" in fv.next_init_case_F:
					next_ic = "1"
				else:
					next_ic = "0"
				fv.consecutive_three_tok_init_case_F = "consec_3_tok_init_case="+prev_ic+curr_ic+next_ic

def generate_combined_feature(Docts):
	for doc in Docts:
		for sent in doc:
			if len(sent)>0:
				sent[0].sent_start_flag = 1

	for doc in Docts:
		for sent in doc:
			for fv in sent:
				z = ""
				if "HL" in fv.Zone_F:
					z = "HL"
				if "AU" in fv.Zone_F:
					z = "AU"
				if "DL" in fv.Zone_F:
					z = "DL"
				if "TXT" in fv.Zone_F:
					z = "TXT"
				if "LOC" in fv.Zone_F:
					z = "LOC"
				if fv.Token[0].isupper():
					if fv.sent_start_flag == 1:
						fv.curr_first_init_cap_Zone_F = "curr_first_init_cap_Zone=11"+z
					else:
						fv.curr_first_init_cap_Zone_F = "curr_first_init_cap_Zone=01"+z
				else:
					if fv.sent_start_flag == 1:
						fv.curr_first_init_cap_Zone_F = "curr_first_init_cap_Zone=10"+z
					else:
						fv.curr_first_init_cap_Zone_F = "curr_first_init_cap_Zone=00"+z
				if fv.Token.isupper():
					fv.curr_all_caps_Zone_F = "curr_all_caps_Zone=1"+z
				else:
					fv.curr_all_caps_Zone_F = "curr_all_caps_Zone=0"+z
				flag_contain_cap = 0
				for i in range(len(fv.Token)):
					if i > 1 and fv.Token[i].isupper():
						flag_contain_cap = 1
						fv.curr_mixed_caps_Zone_F = "curr_mixed_caps_Zone=1"+z
				if flag_contain_cap == 0:
					fv.curr_mixed_caps_Zone_F = "curr_mixed_caps_Zone=0"+z



def feature_builder(filename):		# read file name
	File = open(filename,"r")
	Docts = []
	line = File.readline()
	while 1:
		if not line:
			break
		if "-DOCSTART-" in line:
			doc = []
			line = File.readline()
			while "-DOCSTART-" not in line:
				if not line:
					break
				if "\n" == line:
					sent = []
					line = File.readline()
					while "\n" != line:
						if not line:
							break
						temp = line.split("\t")
						if len(temp) == 4:
							tok, pos, bio, ne = temp
							ne = ne.rstrip("\n")
						else:
							tok, pos, bio = temp
							bio = bio.rstrip("\n")
							ne = "@@"
						f = Feature_Vector (tok, pos, bio, ne)
						sent.append(f)
						line = File.readline()
					doc.append(sent)
			Docts.append(doc)
	File.close()
	return Docts

def valdate_date(tok):
	# regular expression to match dates in format: 2010-08-27 and 2010/08/27 
	date_reg_exp = re.compile(r'(\d{4}[-/]\d{2}[-/]\d{2})$')
	mat = date_reg_exp.match(tok)
	if mat is not None:
		return True
	else:
		return False

def generate_Zone_feature(Docts):
	for doc in Docts:
		flag_find_DL = 0
		for sent in doc:
			for fv in sent:
				if flag_find_DL == 0:
					if valdate_date(fv.Token):
						flag_find_DL = 1
						fv.Zone_F = "Zone=DL"
						for fv in sent:
							if fv.Zone_F != "Zone=DL":
								fv.Zone_F = "Zone=LOC"
				else: 
					fv.Zone_F = "Zone=TXT"
		if flag_find_DL == 1:
			for fv in doc[0]:
				fv.Zone_F = "Zone=HL"
		else:
			for sent in doc:
				for fv in sent:
					fv.Zone_F = "Zone=TXT"
			for fv in doc[0]:
				fv.Zone_F = "Zone=HL"

	for doc in Docts:
		for sent in doc:
			for fv in sent:
				if fv.Zone_F == "Zone=":
					fv.Zone_F = "Zone=AU"

	find_bracket_flag = 0
	for doc in Docts:
		for sent in doc:
			for fv in sent:
				if "{" in fv.Token or "(" in fv.Token or """\"""" in fv.Token or "\'" in fv.Token:
					find_bracket_flag = 1
					fv.curr_sent_has_bracket_or_quotes_F = "curr_sent_has_bracket_or_quotes=1"
			if find_bracket_flag == 1:
				for fv in sent:
					fv.curr_sent_has_bracket_or_quotes_F = "curr_sent_has_bracket_or_quotes=1"

##def get_name_set_from_additional(name_set):
##	with open('data/female_names.csv') as f1:
##	    reader = csv.reader(f1)
##	    for row in reader:
##	    	if float(row[1]) > 0.01 or float(row[1]) == 0.01:
##	        	name_set.add(row[0])
##	with open('data/male_names.csv') as f2:
##	    reader = csv.reader(f2)
##	    for row in reader:
##	    	if float(row[1]) > 0.004:
##	        	name_set.add(row[0])
##	with open('data/last_names.csv') as f3:
##	    reader = csv.reader(f3)
##	    for row in reader:
##	    	if float(row[1]) > 0:
##	        	name_set.add(row[0])

def generate_trigram_feature(Docts):
	for doc in Docts:
		for sent in doc:
			for fv in sent:
				fv.trigram_F = "trigram="+fv.prev_t+"_"+fv.Token+"_"+fv.next_t
				if "upper" in fv.prev_init_case_F and "upper" in fv.next_init_case_F:
					if "upper" in fv.curr_init_case_F:
						fv.cap_case_cap_F = "cap_case_cap=upper"
					else:
						fv.cap_case_cap_F = "cap_case_cap=lower"
				else:
					fv.cap_case_cap_F = "cap_case_cap=null"

def generate_writefile_line(fv):
	line = (fv.Token+"\t"
		+fv.prev_init_case_F+"\t"
		+fv.curr_init_case_F+"\t"
		+fv.next_init_case_F+"\t"
		+fv.prev_tok_F+"\t"
		+fv.curr_tok_F+"\t"
		+fv.next_tok_F+"\t"
		+fv.prev_pos_F+"\t"
		+fv.curr_pos_F+"\t"
		+fv.next_pos_F+"\t"
		+fv.prev_all_upper_case_F+"\t"
		+fv.curr_all_upper_case_F+"\t"
		+fv.next_all_upper_case_F+"\t"
		+fv.curr_lower_case_F+"\t"
		+fv.curr_contain_hyphen_cap_F+"\t"
		+fv.curr_contain_upper_case_F+"\t"
		+fv.curr_contain_dot_F+"\t"
		+fv.curr_contain_quote_cap_F+"\t"
		+fv.curr_contain_number_F+"\t"
		+fv.curr_last_char_is_dot_F+"\t"
		+fv.curr_length+"\t"
		##+fv.curr_word_shape_F+"\t"
		+fv.curr_max_consec_non_vowel_F+"\t"
		+fv.curr_first_init_cap_Zone_F+"\t"
		+fv.curr_all_caps_Zone_F+"\t"
		+fv.curr_mixed_caps_Zone_F+"\t"
		+"sent_start="+str(fv.sent_start_flag)+"\t"
		+fv.curr_sent_has_bracket_or_quotes_F+"\t"
		##+fv.curr_prefix_2+"\t"
		##+fv.curr_suffix_2+"\t"
		##+fv.curr_prefix_3+"\t"
		+fv.curr_suffix_3+"\t"
		+fv.curr_prefix_4+"\t"
		##+fv.curr_suffix_4+"\t"
		##+fv.curr_sent_has_bracket_or_quotes_F+"\t"
		##+fv.rare_word_F+"\t"
		##+fv.in_name_set_F+"\t"
		+fv.curr_bigram_F+"\t"
		##+fv.prev_bigram_F+"\t"
		+fv.trigram_F+"\t"
		+fv.cap_case_cap_F+"\t"
		+fv.Zone_F+"\t"
		+fv.prev_NE_tag_F+"\t"
		+fv.NE+"\n")
	return line

def write_to_txt(Docts,filename):		# write file name
	File = open(filename,"w+")

	doc_start = Feature_Vector("-DOCSTART-", "-X-", "O", "O")
	for doc in Docts:
		File.write(generate_writefile_line(doc_start))
		for sent in doc:
			File.write("\n")
			for fv in sent:
				File.write(generate_writefile_line(fv))
	File.close()
#################################Main#####################################
if len(sys.argv) != 3:
	print("Wrong argument number! it should be:")
	print("python FeatureBuilder.py <input filename> <output_filename>")
else:
	input_filename = sys.argv[1]

	output_filename = sys.argv[2]

	train_docts = feature_builder(input_filename)

	generate_Zone_feature(train_docts)

	generate_curr_feature(train_docts)

	generate_prev_next_feature(train_docts)

	write_to_txt(train_docts,output_filename)


##train_docts = feature_builder("CONLL_train.pos-chunk-name")
##
##generate_Zone_feature(train_docts)
##
##generate_curr_feature(train_docts)
##
##generate_prev_next_feature(train_docts)
##
##write_to_txt(train_docts,"CONLL_train_ENHANCED_FEATURE.txt")
##
##test_docts = feature_builder("CONLL_test.pos-chunk")
##
##generate_Zone_feature(test_docts)
##
##generate_curr_feature(test_docts)
##
##generate_prev_next_feature(test_docts)
##
##write_to_txt(test_docts, "CONLL_test_ENHANCED_FEATURE.txt")

##import difflib
##File1 = open("response.name","r")
##File2 = open("CONLL_dev.name","r")
##lines1 = File1.readlines()
##lines2 = File2.readlines()
##for line in difflib.unified_diff(lines1, lines2, fromfile='file1', tofile='file2', lineterm=''):
##    print line