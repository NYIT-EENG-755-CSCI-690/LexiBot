import random
'''
Neuron Object
'''
class Neuron:
    '''
    state: 1 is 'firing' 0 is 'not firing'
        - Denoted as v_i in the 1982 Hopfield paper
    threshold: used to determin state
        - Denoted as U in the 1982 Hopfield paper
    '''
    def __init__(self, state=0, threshold=0):
        self.state = state
        self.threshold = threshold
    
'''
Neural Network
'''
class Neural_Network:

    def __init__(self, num_neurons, states_set):
        '''
        neurons: A list of all neurons in the network. 
        connection_strengths: Matrix of connection strengths between neurons
            - Denoted T in the 1982 Hopfield paper
            - T_(ij) is the connection strength between neurons i and j
            - T is a symetric matrix because the connection strength
        '''
        self.neurons = [Neuron() for _ in range(num_neurons)]
        self.connection_strengths = [[0 for _ in range(len(self.neurons))] for _ in range(len(self.neurons))]
        self.states_set = states_set
        self.update_connection_strengths()

    def update_neuron_states(self):
        if [neuron.state for neuron in self.neurons] in self.states_set:
            return
        
        loop = True
        k = 0
        while loop:
            for i, neuron_i in enumerate(self.neurons):
                num = 0
                for j, neuron_j in enumerate(self.neurons):
                    if i != j:
                        num += self.connection_strengths[i][j]*neuron_j.state

                v_new = 1 if num >= neuron_i.threshold else 0
                v_old = neuron_i.state

                change_in_enegrgy = self.change_in_energy(v_old, v_new, i)

                neuron_i.state = v_new
                print(f'Change in energy: {change_in_enegrgy} | v_old: {v_old} | v_new: {v_new} | {abs(v_old-v_new)}')
                if [neuron.state for neuron in self.neurons] in self.states_set:
                    print(f'BREAK: {[neuron.state for neuron in self.neurons]}')
                    loop = False
                    break
                if [abs(neuron.state - 1) for neuron in self.neurons] in self.states_set:
                    for neuron in self.neurons:
                        neuron.state = abs(neuron.state - 1)
                    print(f'BREAK CPL: {[neuron.state for neuron in self.neurons]}')
                    loop = False
                    break
                k += 1
    def update_neuron_states_random(self):
        loop = True
        input_seq = [neuron.state for neuron in self.neurons]
        neuron_indicies = [i for i in range(len(self.neurons))]
        k = 0
        while(loop):
            if k >= len(self.neurons):
                for i, neuron in enumerate(self.neurons):
                    neuron.state = input_seq[i]
                    neuron_indicies = [i for i in range(len(self.neurons))]
                k = 0
            
            if neuron_indicies == []:
                neuron_indicies = [i for i in range(len(self.neurons))]

            idx = random.randint(0,len(neuron_indicies)-1)
            i = neuron_indicies[idx]
            neuron_i = self.neurons[i]
            del neuron_indicies[idx]
            num = 0
            for j, neuron_j in enumerate(self.neurons):
                if i != j:
                    num += self.connection_strengths[i][j]*neuron_j.state

            v_new = 1 if num >= neuron_i.threshold else 0
            v_old = neuron_i.state

            change_in_enegrgy = self.change_in_energy(v_old, v_new, i)

            neuron_i.state = v_new
            #print(f'Change in energy: {change_in_enegrgy} | v_old: {v_old} | v_new: {v_new} | {abs(v_old-v_new)}')
            if [neuron.state for neuron in self.neurons] in self.states_set:
                print(f'BREAK: {[neuron.state for neuron in self.neurons]}')
                loop = False
            if [abs(neuron.state - 1) for neuron in self.neurons] in self.states_set:
                for neuron in self.neurons:
                    neuron.state = abs(neuron.state - 1)
                print(f'BREAK CPL: {[neuron.state for neuron in self.neurons]}')
                loop = False
            k += 1
            
    def update_connection_strengths(self):
        for i in range(len(self.connection_strengths)):
            for j in range(i):
                for state_set in self.states_set:
                    self.connection_strengths[i][j] += (2*state_set[i]-1)*(2*state_set[j]-1)
                self.connection_strengths[j][i] = self.connection_strengths[i][j]
                
    def get_energy(self):
        energy = 0

        for i, neuron_i in enumerate(self.neurons):
            for j, neuron_j in enumerate(self.neurons):
                if i != j:
                    energy += self.connection_strengths[i][j]*neuron_i.state * neuron_j.state * -0.5
        
        return energy

    def change_in_energy(self, v_old, v_new, i):
        delta_E = 0
        
        for j, neuron in enumerate(self.neurons):
            if i != j:
                delta_E += self.connection_strengths[i][j]*neuron.state

        delta_E *= (v_new - v_old)

        return delta_E
    
# NEW CLASS

class Text_Processor:
    def __init__(self, words):
        self.words = words
        
        binary_words, num_neurons = self.words_to_binary(self.words)
        states_set = [self.bin_str_to_list(bin_word) for bin_word in binary_words]

        self.neural_network = Neural_Network(num_neurons, states_set)

            
    def word_to_binary(self, word):
        binary_word = ''.join(format(ord(c), '08b') for c in word)
        print(binary_word)
        return binary_word

    def bin_to_word(self, binary_word):
        byte_word = int(binary_word, 2).to_bytes((len(binary_word) + 7) // 8, byteorder='big')
        recovered_word = byte_word.decode()
        return recovered_word

    def words_to_binary(self, words):
        binary_words = [self.word_to_binary(word) for word in words]

        max_bits = 0
        for bin_word in binary_words:
            max_bits = len(bin_word) if max_bits < len(bin_word) else max_bits
        
        #binary_words = [bin_word.zfill(max_bits) for bin_word in binary_words]
        return binary_words, max_bits

    def bin_str_to_list(self, bin_str):
        return [int(bit) for bit in bin_str]

    def list_to_bin_str(self, bin_list):
        return(''.join(str(bit) for bit in bin_list))

    def process_sentence(self, sentence):
        pass

    def process_word(self, word):
        in_word = self.word_to_binary(word).zfill(len(self.neural_network.neurons))
        in_word = self.bin_str_to_list(in_word)

        out_words = {}
        for i in range(10):
            for bit, neuron in zip(in_word, self.neural_network.neurons):
                neuron.state = bit

            self.neural_network.update_neuron_states_random()

            out_word = self.list_to_bin_str([neuron.state for neuron in self.neural_network.neurons])
            out_word = self.bin_to_word(out_word)

            if out_word not in out_words:
                out_words[out_word] = 1
            else:
                out_words[out_word] += 1

        most = sorted(list(out_words.values()))[len(out_words)-1]
        idx = list(out_words.values()).index(most)
        out_word = list(out_words.keys())[idx]

        return(word, out_word)