# Imports
import streamlit as st
import pandas as pd
from dataclasses import dataclass
from datetime import datetime
from typing import Any, List
import hashlib

# Create a Block class to store the date, creator_id, hash, and timestamp


@dataclass
class Block:
    data: Any
    creator_id: int
    timestamp: str = datetime.utcnow().strftime("%H:%M:%S")
    prev_hash: str = "0"
    nonce: int = 0

    # Create a function to hash the block data
    def hash_block(self):
        sha = hashlib.sha256()

        data = str(self.data).encode()
        sha.update(data)

        creator_id = str(self.creator_id).encode()
        sha.update(creator_id)

        prev_hash = str(self.prev_hash).encode()
        sha.update(prev_hash)

        timestamp = str(self.timestamp).encode()
        sha.update(timestamp)

        nonce = str(self.nonce).encode()
        sha.update(nonce)

        return sha.hexdigest()


@dataclass
class PyChain:
    chain: List[Block]
    difficulty: int = 4

    def proof_of_work(self, block):
        calculate_hash = block.hash_block()
        num_of_zeros = "0" * self.difficulty

        while not calculate_hash.startswith(num_of_zeros):
            block.nonce += 1
            calculate_hash = block.hash_block()

        print("Winning Hash", calculate_hash)
        return block

    def add_block(self, candidate_block):
        block = self.proof_of_work(candidate_block)
        self.chain += [block]

    def is_valid(self):
        block_hash = self.chain[0].hash_block()

        for block in self.chain[1:]:
            if block_hash != block.prev_hash:
                print("Blockchain is invalid!!")
                return False

            block_hash = block.hash_block()

        print("Blockchain is valid")
        return True


@st.cache_resource()
def setup():
    print("Initializing Chain")
    return PyChain([Block(data="Genesis", creator_id=0)])


pychain = setup()

# Write some markdown titles with streamlit on the app
st.markdown("# PyChain")
st.markdown("## Store and hash data in a block")

# Receive input data from the user to put into the blockchain
input_data = st.text_area("Block Data")

difficulty = st.sidebar.slider("Block Difficulty", 1, 5, 2)

# Update the `difficulty` data attribute of the `PyChain` data class (`pychain.difficulty`)
# with this new `difficulty` value
pychain.difficulty = difficulty


if st.button("Add Block"):
    prev_block = pychain.chain[-1]
    prev_block_hash = prev_block.hash_block()

    new_block = Block(data=input_data, creator_id=42,
                      prev_hash=prev_block_hash)

    pychain.add_block(new_block)

    st.write("Winning Hash", new_block.hash_block())

st.markdown("## PyChain Ledger")
pychain_df = pd.DataFrame(pychain.chain)

st.write(pychain_df)

if st.button("Validate Blockchain"):
    st.write(pychain.is_valid())

# # Create a button and add the a newly created Block object with all the date inside
# if st.button("Add and Hash Block"):
#     new_block = Block(data=input_data, creator_id=42, hash='')
#     hashed_block = new_block.hash_block()
#     st.write("New Block Fingerprint", hashed_block)
