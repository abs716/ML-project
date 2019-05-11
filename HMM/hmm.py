import string

# five elements for HMM

'''
states = ('Healthy', 'Fever')

observations = ('normal', 'cold', 'dizzy')

start_probability = {'Healthy': 0.6, 'Fever': 0.4}

transition_probability = {
    'Healthy': {'Healthy': 0.7, 'Fever': 0.3},
    'Fever': {'Healthy': 0.4, 'Fever': 0.6},
}

emission_probability = {
    'Healthy': {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
    'Fever': {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6},
}
'''

observations = set()
states = set()
start_probability = dict()
transition_probability = dict()
emission_probability = dict()


def list2probabilitydict(given_list):
    probability_dict = {}
    given_list_length = len(given_list)
    for item in given_list:
        probability_dict[item] = probability_dict.get(item, 0) + 1
    for key, value in probability_dict.items():
        probability_dict[key] = value / given_list_length
    return probability_dict


def Viterbit(obs, states, s_pro, t_pro, e_pro):
    path = {s: [] for s in states}  # init path: path[s] represents the path ends with s
    curr_pro = {}
    for s in states:
        #print(curr_pro[s])
        #print(s_pro[s])
        #print(e_pro[s])
        #print(obs[0])
        #print(e_pro[s][obs[0]])
        curr_pro[s] = s_pro[s] * e_pro[s][obs[0]]
    for i in range(1, len(obs)):
        last_pro = curr_pro
        curr_pro = {}
        for curr_state in states:
            max_pro, last_sta = max(
                ((last_pro[last_state] * t_pro[last_state][curr_state] * e_pro[curr_state][obs[i]], last_state)
                 for last_state in states))
            curr_pro[curr_state] = max_pro
            path[curr_state].append(last_sta)

    # find the final largest probability
    max_pro = -1
    max_path = None
    for s in states:
        path[s].append(s)
        if curr_pro[s] > max_pro:
            max_path = path[s]
            max_pro = curr_pro[s]
            # print '%s: %s'%(curr_pro[s], path[s]) # different path and their probability
    return max_path


if __name__ == '__main__':
    validation_split = 0.2
    training_size = 137860 * 0.8
    validation_size = 1 - training_size
    obs = ['new', 'jersey', 'is', 'sometimes', 'quiet', 'during', 'autumn']
    #obs = ['normal', 'cold', 'dizzy']
    #tokens, tokens2 = []
    #states.add('END')
    fo = open('small_vocab_fr.txt', encoding='utf8')
    ln = 0
    for enLine in open('small_vocab_en.txt', encoding='utf8'):
        ln += 1

        #if ln > training_size:
        #    break

        frLine = fo.readline()

        enTokens = enLine.strip().split(' ')
        #print(enTokens)
        enTokensLength = len(enTokens)
        frTokens = frLine.strip().split(' ')
        frTokensLength = len(frTokens)

        start_probability[frTokens[0]] = start_probability.get(frTokens[0], 0) + 1

        for i in range(0, enTokensLength):
            #enTokens[i] = enTokens[i].strip()
            if enTokens[i] == '':
                continue

            observations.add(enTokens[i])

        for i in range(0, frTokensLength):
            #frTokens[i] = frTokens[i].strip()
            if frTokens[i] == '':
                continue

            states.add(frTokens[i])

            if frTokens[i] not in transition_probability:
                transition_probability[frTokens[i]] = dict()

            if i == frTokensLength - 1:
                nextToken = 'END'
            else:
                nextToken = frTokens[i + 1]
                #nextToken = nextToken.strip()

            transition_probability[frTokens[i]][nextToken] = transition_probability[frTokens[i]].get(nextToken, 0) + 1

            if frTokens[i] not in emission_probability:
                emission_probability[frTokens[i]] = dict()

            if i <= enTokensLength - 1:
                emission_probability[frTokens[i]][enTokens[i]] = emission_probability[frTokens[i]].get(enTokens[i], 0) + 1



    for state in states:
        if state not in start_probability.keys():
            start_probability[state] = 0
        for key, value in transition_probability.items():
            if state not in value.keys():
                transition_probability[key][state] = 0

    for ob in observations:
        for key, value in emission_probability.items():
            if ob not in value.keys():
                emission_probability[key][ob] = 0


    start_probability_total = sum(start_probability.values())
    for key, value in start_probability.items():
        start_probability[key] = value / start_probability_total

    for prev_word, next_word_list in transition_probability.items():
        transition_probability[prev_word] = list2probabilitydict(next_word_list)

    for prev_word, next_word_list in emission_probability.items():
        emission_probability[prev_word] = list2probabilitydict(next_word_list)

    #print(observations)
    #print(states)
    #print(start_probability)
    #print(transition_probability)
    #print(emission_probability)

    print(len(observations))
    print(len(states))
    print(len(start_probability))
    print(len(transition_probability))
    for k, v in transition_probability.items():
        print('T ', len(v))
    print(len(emission_probability))
    for k, v in emission_probability.items():
        print('E ', len(v))

    print(Viterbit(obs, states, start_probability, transition_probability, emission_probability))