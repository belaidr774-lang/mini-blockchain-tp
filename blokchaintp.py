import hashlib
import time

# ------------------------------------------------------
#  STEP 1 — Block Class
# ------------------------------------------------------
class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()

    # ------------------------------------------------------
    # STEP 2 — Compute Hash
    # ------------------------------------------------------
    def compute_hash(self):
        block_string = (
            str(self.index)
            + str(self.timestamp)
            + str(self.data)
            + str(self.previous_hash)
            + str(self.nonce)
        )
        return hashlib.sha256(block_string.encode()).hexdigest()


# ------------------------------------------------------
#  STEP 3 & 4 — Blockchain Class + Proof-of-Work
# ------------------------------------------------------
class Blockchain:
    difficulty = 4  # number of "0" required at start of hash

    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    # Genesis Block
    def create_genesis_block(self):
        genesis = Block(0, "Genesis Block", "0")
        genesis.hash = self.proof_of_work(genesis)
        self.chain.append(genesis)

    # ------------------------------------------------------
    # STEP 4 — Proof-of-Work (Mining)
    # ------------------------------------------------------
    def proof_of_work(self, block):
        required_prefix = "0" * Blockchain.difficulty

        while True:
            computed_hash = block.compute_hash()
            if computed_hash.startswith(required_prefix):
                return computed_hash
            block.nonce += 1

    # ------------------------------------------------------
    # STEP 3 — Add Block
    # ------------------------------------------------------
    def add_block(self, data):
        index = len(self.chain)
        previous_hash = self.chain[-1].hash

        new_block = Block(index, data, previous_hash)
        new_block.hash = self.proof_of_work(new_block)

        self.chain.append(new_block)
        return new_block

    # ------------------------------------------------------
    # STEP 5 — Validate Chain
    # ------------------------------------------------------
    def is_chain_valid(self):
        required_prefix = "0" * Blockchain.difficulty

        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # 1. Previous hash must match
            if current.previous_hash != previous.hash:
                return False

            # 2. Hash must respect difficulty
            if not current.hash.startswith(required_prefix):
                return False

            # 3. Hash must be correct
            if current.hash != current.compute_hash():
                return False

        return True


# ------------------------------------------------------
#  DEMO — RUN THE BLOCKCHAIN (for screenshots)
# ------------------------------------------------------
if __name__ == "__main__":
    bc = Blockchain()

    print("\nMining block 1...")
    bc.add_block("First block data")

    print("Mining block 2...")
    bc.add_block("Second block data")

    print("\nFull Blockchain:\n")
    for block in bc.chain:
        print("---------------")
        print(f"Index: {block.index}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Data: {block.data}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Hash: {block.hash}")
        print(f"Nonce: {block.nonce}")

    # Validation
    print("\nIs chain valid?", bc.is_chain_valid())
