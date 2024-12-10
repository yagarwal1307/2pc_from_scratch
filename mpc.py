from garbled_circuits import label_table, garble_table, eval_garbeled_table
from gen_rsa_params import gen_rsa_params
from random import getrandbits

# NOTE: It's an interactive protocol. Copying some of the code from oblivious transfer file
# Steps:
# Alice would calculate the labeled table, labels, garbled table
# She would send the garbrled table to bob and bob gets label corresponding to his input value 
# Alice will run oblivious transfer protocol with bob to give bob the value of their required input b0/b1
# bob would run evaluate the output label using the garbled circuit and their label and give it to alice
# alice would publish the result


def mpc_alice(logic_table, input_names, output_name, k=128, nbits=2048):
    a = 1 #assuming a's chosen value is 0. This would be replaced by an input

    e, d, N = gen_rsa_params()
    print('Alice generated RSA params...')
    labeled_table, labels = label_table(logic_table, output_name, input_names, k)
    garbled_table = garble_table(labeled_table, k)
    print('Alice computed labeles, labeled table and garbled table...')

    m0, m1 = labels['B'][0], labels['B'][1]
    x0, x1 = getrandbits(nbits), getrandbits(nbits)
    v = yield(x0, x1, e, N, garbled_table, labels['A'][a])
    k0 = pow(v-x0, d, N)
    k1 = pow(v-x1, d, N)
    m0k = (m0 + k0) % N
    m1k = (m1 + k1) % N
    output_label = yield m0k, m1k

    output = 0
    if (labels[output_name][0] != output_label):
        output = 1
    
    print('Alice calculated output using output label...')

    yield output

def mpc_bob(nbits=2048):
    b = 1 #Assuming b's chosen value is 1

    x0, x1, e, N, garbled_table, alice_label = yield
    print('Bob received parameters and garbled table...')
    k = getrandbits(nbits)
    v = ((x0, x1)[b] + pow(k, e, N)) % N
    m0k, m1k = yield v
    bob_label = ((m0k, m1k)[b] - k) % N
    print('Bob received his label...')

    output_label = eval_garbeled_table(garbled_table, (alice_label, bob_label))
    print('Bob calculated output label...')
    yield output_label
    

def mpc(alice, bob):
    x0, x1, e, N, garbled_table, alice_label = next(alice)
    next(bob)
    v = bob.send((x0, x1, e, N, garbled_table, alice_label))
    m0k, m1k = alice.send(v)
    output_label = bob.send((m0k, m1k))
    output = alice.send(output_label)
    return output, output_label

if __name__ == '__main__':
    logic_table_and_gate = [[0, 0], [0, 1]]
    mpca = mpc_alice(logic_table_and_gate, ['A', 'B'], 'out')
    mpcb = mpc_bob()
    output, output_label = mpc(mpca, mpcb)

    print('Output: ', output)
    print('Output Label: ', output_label)


