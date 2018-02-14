"""
@Assignment : Artificial Intelligence assignment 1
@Aurthor Utkarsh Gera

@Explaination
The program bascially searches the search space in bfs manner from both the ends, start as well as the goal state.
The program takes the input KB and divides KB into two parts - atomic sentence, which contains a predicate and other as rule containing 
multiple predicates. It then starts to generate all the possible combinations from the given KB(Foward approach) keeping
in mind that the three statements being combined satisfy the following two conditions
1. A predicate is removed when the output of the two statements is generated ie the predicate and its complement must be present in 
1st statement and 2nd statement or vice versa.
2.Variable Unification - When two statements are reduced together to form a new one variable unification must take place. Either the
variable must be substituted with a constant or another variable, depending upon the predicate used for reduction. So if the predicate contains
a constant the its complementary predicate must either contain a variable or the same constant to reduce the predicate.
3. The two statements combining must not share each others parent sentences or themselves as parent for other, from which they have
blood ties. It is like a family, none of the children must marry within the family. This condition makes sure that the KB ends 
generating new sentences when all the combinations are exhausted.

The last condition also help us in eliminating the condition of self loops since it won't allow statements with common parents to be
used for reduction.

The above mentioned step is bascially exploring from the start state. Now for the search from goal state. Since all the possible 
search space was explored from given KB, the query(atomic query) we are looking/searching should be present in the KB as a independent 
sentence. However if in case it is not present, use the complement of the query and try to reduce it with one of the rule sentences from
the KB. If it gets reduced then use the remnant and try to reduce it with all the atomic sentences present in the KB, basically to prove
that the KB is inconsistent when complement of the query is put in KB meaning that the query is valid. If we are successful in
eliminating all the predicates from the sentence we will get null/empty predicate sentence in the in the end. 
"""

class KB(object):
    """
    Initializes the KB , query and the KB indexers
    """
    def __init__(self):
        # Array of the knowledge base
        self.kb = []

        # Array of the queries
        self.query = []

        # indexing the knowledge base
        self.indexing = dict({
            '$': dict({
                'atomic': dict({}),
                'rule': dict({})
            }),
            '~': dict({
                'atomic': dict({}),
                'rule': dict({})
            }),
        })

        self.matched_kb = dict({})
        self.origins_kb = dict({})

    type_switch = dict({
        '$': '~',
        '~': '$'
    })

    loop_type_switch = dict({
        '$': '~',
        '~': None
    })

    loop_p_switch = dict({
        'atomic': 'rule',
        'rule': None
    })

    """
    Expands the KB with all the permutations possible from it.
    """
    def expand_kb(self):
        kb_size = 0
        while kb_size < len(self.kb):
            # Update the new KB size
            kb_size = len(self.kb)

            # Pick off the sentences one by one
            for s_index in range(len(self.kb)):
                # Sentence in question
                sentence = self.kb[s_index]

                # Map which all statements it was mapped with
                if self.matched_kb.get(s_index) is None:
                    self.matched_kb[s_index] = dict({})
                    # No reduction with yourself
                    self.matched_kb[s_index][s_index] = True

                # Start with some predicate type
                negation = '$'

                while negation is not None:
                    # Pick up the negation predicates of the sentence one by one
                    for predicate_name in sentence[negation]:

                        # Loop on its argument list present
                        for instance_index in range(len(sentence[negation][predicate_name])):

                            # --------------------------------- Counter Sentence from KB for atomic ------------------------
                            self.kb_match_finder(negation, predicate_name, sentence, instance_index, 'atomic', s_index)

                            # ---------------------------------- Counter Sentence from KB for rule ------------------------
                            self.kb_match_finder(negation, predicate_name, sentence, instance_index, 'rule', s_index)

                    negation = self.loop_type_switch[negation]

    """
    Tries to find a match inside the KB for a predicate
    """
    def kb_match_finder(self, negation, predicate_name, sentence, instance_index, s_type, s_index):
        # Try and couple it with its complement in the KB by referring the indexer
        if self.indexing[self.type_switch[negation]][s_type].get(predicate_name) is not None:
            # If an entry is present in the indexer
            for counter_index in self.indexing[self.type_switch[negation]][s_type][predicate_name]:
                # Check if this sentence was matched with the sentence in question in the past
                if self.matched_kb[s_index].get(counter_index) is None:

                    # Now it is matched once
                    self.matched_kb[s_index][counter_index] = True

                    # Put the same for its counter sentence
                    if self.matched_kb.get(counter_index) is None:
                        self.matched_kb[counter_index] = dict({})
                        # No reduction with yourself
                        self.matched_kb[counter_index][counter_index] = True
                    self.matched_kb[counter_index][s_index] = True

                    # Now check both the sentences origins
                    common_origins = False
                    for origin in self.origins_kb[s_index]:
                        if origin in self.origins_kb[counter_index]:
                            common_origins = True
                            break

                    # If both the statements share a common origin then move on
                    if common_origins:
                        continue

                    # Fetch the sentence from the KB
                    counter_sentence = self.kb[counter_index]

                    for counter_args_index in range(len(counter_sentence[self.type_switch[negation]][predicate_name])):
                        result, unique = self.is_unify(sentence[negation][predicate_name][instance_index],
                                                       counter_sentence[self.type_switch[negation]][predicate_name][
                                                         counter_args_index])

                        if result is not None:
                            new_sentence = self.unification(result, unique, predicate_name, sentence,
                                                            counter_sentence, instance_index, counter_args_index, negation)

                            # Inconsistent KB check
                            if new_sentence['p_count'] > 0:
                                # Check whether this sentence already exists in the KB
                                result = self.is_duplicate(new_sentence)

                                # Unique sentence
                                if not result:
                                    # Create an entry of the creators of this sentence to restrict future matches
                                    self.matched_kb[len(self.kb)] = dict({})
                                    self.matched_kb[len(self.kb)][s_index] = True
                                    self.matched_kb[len(self.kb)][counter_index] = True

                                    # No reduction with yourself
                                    self.matched_kb[len(self.kb)][len(self.kb)] = True

                                    self.matched_kb[s_index][len(self.kb)] = True
                                    self.matched_kb[counter_index][len(self.kb)] = True

                                    # Keep a track about it origin sentences
                                    self.origins_kb[len(self.kb)] = []
                                    self.origins_kb[len(self.kb)].extend(self.origins_kb[s_index])
                                    self.origins_kb[len(self.kb)].extend(self.origins_kb[counter_index])

                                    # Update the indexer
                                    self.indexer_update(new_sentence)
                                    # Append to the KB
                                    self.kb.append(new_sentence)

    """
    Checks whether a newly generated sentence is already present in the KB.
    """
    def is_duplicate(self, new_sentence):
        # Check the sentence type
        if new_sentence['p_count'] > 0:
            s_type = 'rule'
        else:
            s_type = 'atomic'

        if len(new_sentence['~'].keys()) > 0:
            ref_predicate = new_sentence['~'].keys()[0]
            negate_flag = '~'
        else:
            ref_predicate = new_sentence['$'].keys()[0]
            negate_flag = '$'

        # Pick up the possible sentences matching a predicate of the new sentence from the indexer
        for s_index in self.indexing[negate_flag][s_type][ref_predicate]:

            # If the predicate counts in both the sentences match
            if self.kb[s_index]['p_count'] == new_sentence['p_count']:

                # Start with matching each predicates arguments
                negation = '$'
                match_found = True

                # Logically match the variables
                variable_match = dict({})

                while negation is not None:
                    # Pick up predicates name one by one for a particular negation
                    for predicate_name in new_sentence[negation].keys():
                        # Stores the index of the argument list that were used in matching for a predicate
                        used_predicates = dict({})

                        # Argument list from the new sentence
                        for new_arg_list in new_sentence[negation][predicate_name]:
                            # Set default match found
                            match_found = False

                            # KB sentence to check if it has a match for the new_sentence
                            if self.kb[s_index][negation].get(predicate_name) is not None:
                                for kb_arg_list_index in range(len(self.kb[s_index][negation][predicate_name])):

                                    # Check if this was already not used for some matching
                                    if kb_arg_list_index not in used_predicates.keys():

                                        # Try to match the variables for this instance of predicate
                                        predicate_var_map = dict({})

                                        # Change default match found
                                        match_found = True

                                        # Alias for the argument list for that predicate
                                        sen_pred_arg_list = self.kb[s_index][negation][predicate_name][kb_arg_list_index]

                                        # Compare the arguments in both lists for matching
                                        for gen_arg_index in range(len(sen_pred_arg_list)):

                                            # Check both are variables
                                            if sen_pred_arg_list[gen_arg_index].islower() and \
                                                    new_arg_list[gen_arg_index].islower():

                                                # Check for new match for sentence of KB
                                                if variable_match.get(sen_pred_arg_list[gen_arg_index]) is None:

                                                    # No mapping for the query variable exists
                                                    if variable_match.get(new_arg_list[gen_arg_index]) is None:

                                                        # Mutual mapping of the variables
                                                        variable_match[sen_pred_arg_list[gen_arg_index]] = \
                                                            new_arg_list[gen_arg_index]
                                                        variable_match[new_arg_list[gen_arg_index]] = \
                                                            sen_pred_arg_list[gen_arg_index]

                                                        # Entry for current instance for deletion purpose if fail
                                                        predicate_var_map[sen_pred_arg_list[gen_arg_index]] = \
                                                            new_arg_list[gen_arg_index]
                                                    else:
                                                        # Mismatch so break
                                                        for key in predicate_var_map.keys():
                                                            # Mutual deletion
                                                            del variable_match[variable_match[key]]
                                                            del variable_match[key]

                                                        # Condition for a mismatch
                                                        match_found = False
                                                        break
                                                else:

                                                    # There exists a mapping for the sentence variable and its fail
                                                    if not variable_match[sen_pred_arg_list[gen_arg_index]] == new_arg_list[gen_arg_index]:
                                                        # Mismatch so break
                                                        for key in predicate_var_map.keys():
                                                            # Mutual deletion
                                                            del variable_match[variable_match[key]]
                                                            del variable_match[key]

                                                        # Condition for a mismatch
                                                        match_found = False
                                                        break

                                            elif sen_pred_arg_list[gen_arg_index].isupper() and \
                                                    new_arg_list[gen_arg_index].isupper():
                                                # Both are constants and not equal
                                                if not new_arg_list[gen_arg_index] == sen_pred_arg_list[gen_arg_index]:
                                                    for key in predicate_var_map.keys():
                                                        # Mutual deletion
                                                        del variable_match[variable_match[key]]
                                                        del variable_match[key]

                                                    # Condition for a mismatch
                                                    match_found = False
                                                    break
                                            else:
                                                # Mismatch so break variable vs constant
                                                for key in predicate_var_map.keys():
                                                    value = variable_match[key]
                                                    # Mutual deletion
                                                    del variable_match[key]
                                                    del variable_match[value]

                                                # Condition for a mismatch
                                                match_found = False
                                                break

                                        if not match_found:
                                            # No Match found, so skip this predicate instance
                                            continue
                                        else:
                                            # Register this instance
                                            used_predicates[kb_arg_list_index] = True
                                        break

                            # No match with this sentence in KB
                            if not match_found:
                                break

                        # No use here, pick up a new sentence from KB
                        if not match_found:
                            break

                    # Now switch to the complement part provided all previous arguments matched
                    if match_found:
                        negation = self.loop_type_switch[negation]
                    else:
                        break

                # Condition if it matched entirely
                if match_found:
                    return True

        return False

    """
    Updates an indexer with the sentence for fast access
    """
    def indexer_update(self, sentence, append=True):
        negation = '$'
        if sentence['p_count'] > 1:
            s_type = 'rule'
        else:
            s_type = 'atomic'

        while negation is not None:
            for predicate_name in sentence[negation].keys():
                if append:
                    if self.indexing[negation][s_type].get(predicate_name) is None:
                        self.indexing[negation][s_type][predicate_name] = []
                    self.indexing[negation][s_type][predicate_name].append(len(self.kb))
                else:
                    self.indexing[negation][s_type][predicate_name] = self.indexing[negation][s_type][predicate_name][:-1]

            negation = self.loop_type_switch[negation]

    """
    Prepares a predicate object and returns it
    """
    @staticmethod
    def predicate_object(s):
        s = s.strip()

        # Prepare a new predicate object
        negate_flag = '$'

        if s[0] is '~':
            negate_flag = '~'
            s = s[1:]

        s = s.split('(')
        predicate_signature = s[0].strip()

        s = s[1].split(')')
        arguments_list = s[0].split(',')

        for arg_index in range(len(arguments_list)):
            arguments_list[arg_index] = arguments_list[arg_index].strip()

        return predicate_signature, negate_flag, arguments_list

    """
    Adds a new sentence object to the KB
    sentence = {
        '~' : {
            p1 : [arg_list1, arg_list2],
            p2 : [arg_list1, arg_list2],
        },
        '$' : {
            p1 : [arg_list1, arg_list2],
            p2 : [arg_list1, arg_list2],
        },
        'p_count' : no of predicates
    }
    """
    def add_new(self, s):
        s = s.split('|')
        index = len(self.kb)

        sentence = dict({
            '~': dict({}),
            '$': dict({}),
            'p_count': len(s)
        })

        std_variable = dict({})
        count = 1

        if len(s) > 1:
            s_type = 'rule'
        else:
            s_type = 'atomic'

        # Give index of its origin which is itself
        self.origins_kb[len(self.kb)] = [len(self.kb)]

        for k in s:
            literal_name, l_negate, l_args = KB.predicate_object(k)

            for arg_index in range(len(l_args)):
                if l_args[arg_index][0].islower() and std_variable.get(l_args[arg_index]) is None:
                    std_variable[l_args[arg_index]] = 'v' + str(index) + '$' + str(count)
                    count += 1

                if not l_args[arg_index][0].isupper():
                    l_args[arg_index] = std_variable[l_args[arg_index]]

            if self.indexing[l_negate][s_type].get(literal_name) is None:
                self.indexing[l_negate][s_type][literal_name] = []

            # Index the predicate
            self.indexing[l_negate][s_type][literal_name].append(index)

            # Create predicate entry in the sentence
            if sentence[l_negate].get(literal_name) is None:
                sentence[l_negate][literal_name] = []

            # Append the new argument list to the predicate
            sentence[l_negate][literal_name].append(l_args)

        # Add the predicate to the KB
        self.kb.append(sentence)

    """
    Searches the KB for reducing a sentence
    """
    def search_kb(self, curr_query):
        if curr_query['p_count'] > 0:
            # Search if the query already exists in the KB
            negation = '$'

            while negation is not None:
                # If there is predicate for this negation
                if len(curr_query[negation].keys()) > 0:
                    predicate_name = curr_query[negation].keys()[0]
                    query_arg_list = curr_query[negation][predicate_name][0]

                    # Check if this value was derived after KB expansion
                    if self.indexing[self.type_switch[negation]]['atomic'].get(predicate_name):
                        for index in self.indexing[self.type_switch[negation]]['atomic'][predicate_name]:
                            sentence = self.kb[index]
                            result, unique = self.is_unify(query_arg_list,
                                                           sentence[self.type_switch[negation]]
                                                           [predicate_name][0])

                            if result is not None:
                                return True
                negation = self.loop_type_switch[negation]
        else:
            # Empty query is true
            return True

        # Even after expansion there was no suitable match
        negation = '$'

        while negation is not None:
            # If there is predicate for this negation
            if len(curr_query[negation].keys()) > 0:
                predicate_name = curr_query[negation].keys()[0]
                query_arg_list = curr_query[negation][predicate_name][0]

                # Check if the predicate really exists in the index
                if self.indexing[self.type_switch[negation]]['rule'].get(predicate_name):
                    for index in reversed(self.indexing[self.type_switch[negation]]['rule'][predicate_name]):
                        sentence = self.kb[index]

                        # Match the query with all the possible argument lists of that predicate
                        for arg_list_index in range(len(sentence[self.type_switch[negation]]
                                                       [predicate_name])):
                            result, unique = self.is_unify(query_arg_list,
                                                           sentence[self.type_switch[negation]]
                                                           [predicate_name][arg_list_index])

                            # Matches with the predicate, Proceed for the reducto
                            if result is not None:
                                new_sentence = self.unification(result, unique, predicate_name, curr_query,
                                                                sentence, 0, arg_list_index, negation)
                                # As per the rule, add to the KB. No need for indexer
                                self.kb.append(new_sentence)

                                # Will contain at least one predicate since it was picked from rule
                                result = self.reducto(new_sentence)

                                # Remove the newly added sentence
                                self.kb = self.kb[:-1]

                                if result:
                                    return True

            negation = self.loop_type_switch[negation]

        return False

    """
    Tries to reduces the queries with the atomic sentences
    """
    def reducto(self, curr_query):
        # Start from somewhere
        negation = '$'

        while negation is not None:
            # If there is predicate for this negation
            if len(curr_query[negation].keys()) > 0:
                # Pick up the first predicate name
                predicate_name = curr_query[negation].keys()[0]
                query_arg_list = curr_query[negation][predicate_name][0]

                # Check if the predicate really exists in index
                if self.indexing[self.type_switch[negation]]['atomic'].get(predicate_name):
                    for index in reversed(self.indexing[self.type_switch[negation]]['atomic'][predicate_name]):
                        atomic = self.kb[index]
                        result, unique = self.is_unify(query_arg_list,
                                                       atomic[self.type_switch[negation]]
                                                       [predicate_name][0])

                        if result is not None:
                            # If query has only one predicate and unification is true
                            if curr_query['p_count'] == 1:
                                return True
                            else:
                                # Unify the sentence and try to reduce further
                                new_sentence = self.unification(result, unique, predicate_name, curr_query,
                                                                atomic, 0, 0, negation)

                                # As per the rule, add to the KB. No need for indexer
                                self.kb.append(new_sentence)

                                # Will contain at least one predicate since it was picked from rule
                                result = self.reducto(new_sentence)

                                # Remove the newly added sentence
                                self.kb = self.kb[:-1]

                                if result:
                                    return True
            negation = self.loop_type_switch[negation]

        return False

    """
    Whether unification between the 2 sentences arguments is possible
    """
    def is_unify(self, arg_list1, arg_list2):
        mapper = dict({})
        unique = 1

        for index in range(len(arg_list1)):
            if arg_list1[index][0].isupper() and arg_list1[index] == arg_list2[index]:
                # Both are constants and equal
                pass
            elif arg_list1[index][0].islower():
                if arg_list2[index][0].islower():
                    # Both are variables
                    if mapper.get(arg_list1[index]) is None and mapper.get(arg_list2[index]) is None:
                        mapper[arg_list1[index]] = 'v' + str(len(self.kb)) + '$' + str(unique)
                        mapper[arg_list2[index]] = 'v' + str(len(self.kb)) + '$' + str(unique)
                        unique += 1
                    elif mapper.get(arg_list1[index]) is None:
                        mapper[arg_list1[index]] = mapper[arg_list2[index]]
                    elif mapper.get(arg_list2[index]) is None:
                        mapper[arg_list2[index]] = mapper[arg_list1[index]]
                    else:
                        mapper[mapper[arg_list1[index]]] = 'v' + str(len(self.kb)) + '$' + str(unique)
                        mapper[mapper[arg_list2[index]]] = 'v' + str(len(self.kb)) + '$' + str(unique)
                        unique += 1

                else:
                    # It is a constant value
                    mapper[arg_list1[index]] = arg_list2[index]
            elif arg_list2[index][0].islower():
                # It is a constant value in arg_list1
                mapper[arg_list2[index]] = arg_list1[index]
            else:
                # Two different constants
                return None, None

        return mapper, unique

    '''
    Will call this place to unify the given two sentences
    '''
    def unification(self, variable_substitution, unique, predicate_name, sentence,
                    counter_sentence, instance_index, counter_args_index, original_negation):
        resultant_sentence = dict({
            '$': dict({}),
            '~': dict({}),
            'p_count': 0
        })

        # Normalize the variable substitutions
        stack = []
        for initial_variables in variable_substitution.keys():
            value = variable_substitution.get(variable_substitution[initial_variables])
            while variable_substitution.get(value) is not None:
                stack.append(value)
                value = variable_substitution[value]

            for val in stack:
                variable_substitution[val] = value
            stack = []

        # ------------------------------- First for the normal query then for its counter part -----------------------
        negation = '$'
        # For both the negated and the normal sentence
        while negation is not None:
            # Select the predicates
            for predicate in sentence[negation].keys():
                # Select an argument list of that predicate
                for arg_list_index in range(len(sentence[negation][predicate])):
                    # Check if it is not the same as the reduced predicate
                    if not original_negation == negation or not predicate == predicate_name \
                            or not arg_list_index == instance_index:
                        # Check if the resultant sentence has that predicate entry
                        if resultant_sentence[negation].get(predicate) is None:
                            resultant_sentence[negation][predicate] = []

                        # Increase the predicate count
                        resultant_sentence['p_count'] += 1

                        # Prepare a new argument list
                        new_arg_list = []
                        for arg in sentence[negation][predicate][arg_list_index]:
                            if arg[0].islower():
                                # If that variable was not assigned a value
                                if variable_substitution.get(arg) is None:
                                    variable_substitution[arg] = 'v' + str(len(self.kb)) + '$' + str(unique)
                                    unique += 1
                                # Put that value in the new arg list
                                new_arg_list.append(variable_substitution[arg])
                            else:
                                # It is a constant
                                new_arg_list.append(arg)

                        # Add the new argument list
                        resultant_sentence[negation][predicate].append(new_arg_list)
            negation = self.loop_type_switch[negation]

        # For both the negated and the normal sentence
        negation = '$'
        while negation is not None:
            # Select the predicates
            for predicate in counter_sentence[negation].keys():
                # Select an argument list of that predicate
                for arg_list_index in range(len(counter_sentence[negation][predicate])):
                    # Check if it is not the same as the reduced predicate
                    if not self.type_switch[original_negation] == negation or not predicate == predicate_name \
                            or not arg_list_index == counter_args_index:
                        # Check if the resultant sentence has that predicate entry
                        if resultant_sentence[negation].get(predicate) is None:
                            resultant_sentence[negation][predicate] = []

                        # Increase the predicate count
                        resultant_sentence['p_count'] += 1

                        # Prepare a new argument list
                        new_arg_list = []
                        for arg in counter_sentence[negation][predicate][arg_list_index]:
                            if arg[0].islower():
                                # If that variable was not assigned a value
                                if variable_substitution.get(arg) is None:
                                    variable_substitution[arg] = 'v' + str(len(self.kb)) + '$' + str(unique)
                                    unique += 1
                                # Put that value in the new arg list
                                new_arg_list.append(variable_substitution[arg])
                            else:
                                # It is a constant
                                new_arg_list.append(arg)

                        # Add the new argument list
                        resultant_sentence[negation][predicate].append(new_arg_list)
            negation = self.loop_type_switch[negation]

        return resultant_sentence

"""
Read file function
"""
def read_file():
    input_file = open('input.txt', 'r')
    count = int(input_file.readline())

    '''
    Query parser
    '''

    for i in range(count):
        temp = input_file.readline()
        literal_name, l_negate, l_args = KB.predicate_object(temp)
        l_negate = KB.type_switch[l_negate]
        single_query = dict({
            '$': dict({}),
            '~': dict({}),
            'p_count': 1
        })
        single_query[l_negate][literal_name] = []
        single_query[l_negate][literal_name].append(l_args)
        kb.query.append(single_query)

    '''
    Knowledge Base preparation
    '''
    count = int(input_file.readline())

    for i in range(count):
        temp = input_file.readline()
        kb.add_new(temp)


if __name__ == '__main__':
    kb = KB()

    # Parse the input file
    read_file()

    # Discover all the other possible combinations in the KB
    kb.expand_kb()

    # Output file reference
    output_file = open('output.txt', 'w')

    # Start the query answering engine
    for query in kb.query:
        # As per the rule, add to the KB and the indexer
        kb.indexer_update(query)
        kb.kb.append(query)

        # Fetch an answer to the query
        answer = kb.search_kb(query)

        # Remove the query statement
        kb.indexer_update(query, False)
        kb.kb = kb.kb[:-1]

        if answer:
            output_file.write('TRUE\n')
        else:
            output_file.write('FALSE\n')
