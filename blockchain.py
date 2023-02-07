#pip install Flask==0.12.2 requests==2.18.4 

'''
Primero crearemos una Blockchainclase cuyo constructor crea una lista vacía inicial 
(para almacenar nuestra cadena de bloques) y otra para almacenar transacciones
'''

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        
    def new_block(self):
        # Creates a new Block and adds it to the chain
        pass
    
    def new_transaction(self):
        # Adds a new transaction to the list of transactions
        pass
    
    @staticmethod
    def hash(block):
        # Hashes a Block
        pass

    @property
    def last_block(self):
        # Returns the last Block in the chain
        pass

'''
Nuestra Blockchainclase es responsable de administrar la cadena. 
Almacenará transacciones y tendrá algunos métodos auxiliares para agregar nuevos bloques a la cadena. 
Cada bloque tiene un índice , una marca de tiempo (en tiempo de Unix), una lista de transacciones, 
una prueba (más sobre eso más adelante) y el hash del bloque anterior .
'''

block = {
    'index': 1,
    'timestamp': 1506057125.900785,
    'transactions': [
        {
            'sender': "8527147fe1f5426f9dd545de4b27ee00",
            'recipient': "a77f5cdfa2934df3954a5c7c7da5df1f",
            'amount': 5,
        }
    ],
    'proof': 324984774000,
    'previous_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
}


'''
Cada nuevo bloque contiene dentro de sí mismo, el hash del bloque anterior. 
Esto es crucial porque es lo que le da inmutabilidad a las cadenas de bloques: si un atacante corrompió 
un bloque anterior en la cadena, todos los bloques posteriores contendrán hashes incorrectos.
'''

'''
Necesitaremos una forma de agregar transacciones a un Bloque. 
Nuestro método new_transaction() es responsable de esto, y es bastante sencillo:
'''

class Blockchain(object):
    ...
    
    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

'''
Después de agregamos new_transaction() que sera la transacción que ira al siguiente bloque, 
agregandose  al índice del bloque siguiente que se extraerá. 
Esto será útil más adelante, para el usuario que envía la transacción.
'''
#---------------------------------------------------------------------#

'''
Cuando  crea una blockchain, necesitamos un bloque de génesis, es decir,
un bloque sin predecesores. También necesitaremos agregar una "prueba" a nuestro bloque génesis que 
es el resultado de la minería (o prueba de trabajo). 

Además de crear el bloque de génesis en nuestro constructor, también desarrollaremos los métodos
para nuevo_bloque(), nueva_transaccion() y el hash().

En codigo lo visualizaremos en ingles ➡️ new_block(), new_transaction() y hash():
'''

import hashlib
import json
from time import time


class Blockchain(object):
    def __init__(self):
        self.current_transactions = []
        self.chain = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()



'''
Y.. ¿cómo se crean, forjan o extraen nuevos bloques? Sencillo, a traves de un algoritmo de proof of work.


Este algoritmo de prueba de trabajo (PoW) crea o extrae nuevos bloques en la cadena de bloques. 
El objetivo de PoW es descubrir un número que resuelva un problema. 
El número debe ser difícil de encontrar
pero fácil de verificar —computacionalmente hablando— por cualquiera en la red. 

Veremos un ejemplo:

Decido que el hash de algún entero 'x' multiplicado por otro, debe terminar en 0. 
Entonces, hash(x * y) = ac23dc...0. 
Y para este ejemplo simplificado, arreglemos x = 5. En Python sería:




from hashlib import sha256
x = 5 
y = 0 # Aún no sabemos cuál debería ser y...
while sha256(f'{x*y}'.encode()).hexdigest()[-1] != "0": 
    y += 1
print(f'La solución es y = {y}')

La solución es y=21, ya que el hash producido es 0

hash(5 * 21) = 1253e9373e...5e3600155e860


'''


'''Implementación de Prueba de trabajo básica'''

import hashlib
import json

from time import time
from uuid import uuid4


class Blockchain(object):
    ...
        
    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

'''
Para ajustar la dificultad del algoritmo, podríamos modificar el número de ceros iniciales.
Con 4 es suficiente, ya que con 5 aumentariamos considerablemente el tiempo de espera 
para dar con la solución.
'''


'''
Nuestra clase está casi completa y estamos listos para comenzar a interactuar con ella mediante 
solicitudes HTTP.
Utilizaremos el framework flask y crearemos tres metodos
# /transactions/newpara crear una nueva transacción a un bloque
#/mine para decirle a nuestro servidor que extraiga un nuevo bloque.
#/chain para devolver la Blockchain completa.
'''


'''
Para la configuración de flask, nuestro "servidor" formará un solo nodo en nuestra red blockchain. 
Vamos a crear un código repetitivo:
'''

import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4

from flask import Flask


class Blockchain(object):
    ...


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    return "We'll mine a new Block"
  
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    return "We'll add a new transaction"

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

''''
Aqui explico lo creado anteriormente:

Línea 15: Instancia nuestro Node. 
Línea 18: Crea un nombre aleatorio para nuestro nodo.
Línea 21: Instanciamos nuestra Blockchainclase.
Línea 24–26: Creamos el /minepunto final, que es una GETsolicitud.
Línea 28–30: Creamos el /transactions/newpunto final, que es una POSTsolicitud, ya que le enviaremos datos.
Línea 32–38: Creamos el /chainpunto final, que devuelve la Blockchain completa.
Línea 40–41: Ejecuta el servidor en el puerto 5000
'''



'''
Como ya tenemos nuestro método de clase para agregar transacciones a un bloque, el resto es fácil. 
Escribamos la función para sumar transacciones:
'''

import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request

...

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

'''
Nuestro punto final de minería tiene que hacer tres cosas:

Calcular la prueba de trabajo
Recompensar al minero (nosotros en este caso) agregando una transacción que nos otorgue 1 token
Forjar el nuevo Bloque añadiéndolo a la cadena.
'''

import hashlib
import json

from time import time
from uuid import uuid4

from flask import Flask, jsonify, request

...

@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200



#Ahora interactuaremos con la blockchain#

''''
Podemos usar cURL interactuar con nuestra API a través de una red.

Encendemos el servidor:

$ python blockchain.py
* Ejecutándose en http://127.0.0.1:5000/ (Presione CTRL+C para salir)
Intentemos extraer un bloque haciendo una GETsolicitud a http://localhost:5000/mine:
'''


'''
Ahora tenemos una cadena de bloques básica que acepta transacciones y nos permite 
extraer nuevos bloques. Pero el objetivo de Blockchains es que deberían estar descentralizados. 
Y si están descentralizados, ¿cómo diablos nos aseguramos de que todos reflejen la misma cadena?
Esto se llama el problema del Consenso, y tendremos que implementar un Algoritmo de Consenso si queremos 
más de un nodo en nuestra red.
Antes de que podamos implementar un algoritmo de consenso, necesitamos una forma de informar a un nodo 
sobre los nodos vecinos en la red. Cada nodo de nuestra red debe mantener un registro de otros nodos 
de la red. Por lo tanto, necesitaremos algunos puntos finales más:

/nodes/register para aceptar una lista de nuevos nodos en forma de URL.
/nodes/resolve para implementar nuestro algoritmo de consenso, que resuelve cualquier conflicto, 
para garantizar que un nodo tenga la cadena correcta.
Tendremos que modificar el constructor de nuestra Blockchain y proporcionar un método para registrar nodos
'''

from urllib.parse import urlparse
...


class Blockchain(object):
    def __init__(self):
        ...
        self.nodes = set()
        ...

    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: <str> Address of node. Eg. 'http://192.168.0.5:5000'
        :return: None
        """

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)


#Hay que tener en cuenta que se ha usado set() para contener la lista de nodos# 👀



'''
Un conflicto se da cuando un nodo tiene una cadena diferente a otro nodo. Para resolver esto, 
estableceremos la regla de que la cadena mas larga tiene siempre la autoridad. 
Usando este algoritmo, llegamos a un consenso entre los nodos de nuestra red.
'''

import requests


class Blockchain(object):
    ...
    
    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our Consensus Algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: <bool> True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False


'''
El primer método valid_chain()es responsable de verificar si una cadena es válida al recorrer cada bloque y 
verificar tanto el hash como la prueba.

resolve_conflicts()es un método que recorre todos nuestros nodos vecinos, 
descarga sus cadenas y las verifica utilizando el método anterior. Si se encuentra una cadena válida, 
cuya longitud es mayor que la nuestra, reemplazamos la nuestra.

Registremos los dos puntos finales en nuestra API, uno para agregar nodos vecinos y otro para resolver 
conflictos:

'''

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200

'''
En este punto, podemos coger una máquina diferente (si se desea) y activar diferentes nodos en nuestra red. 
O activar procesos usando diferentes puertos en la misma máquina. 
Active otro nodo en mi maquina, en un puerto diferente, y lo registré con mi nodo actual. 
Por lo que ahora tengo dos nodos: http://localhost:5000y http://localhost:5001.
Luego extraje algunos bloques nuevos en el nodo 2 para asegurarme de que la cadena fuera más larga. 
Luego, llamé GET /nodes/resolveal nodo 1, donde la cadena fue reemplazada por el algoritmo de consenso.
'''

