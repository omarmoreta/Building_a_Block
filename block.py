# Imports
import streamlit as st
from dataclasses import dataclass
from datetime import datetime
from typing import Any
import hashlib

# Create a Block class to store the date, creator_id, hash, and timestamp


@dataclass
class Block:
    data: Any
    creator_id: int
    hash: Any
    timestamp: str = datetime.utcnow().strftime("%H:%M:%S")

    # Create a function to hash the block data
    def hash_block(self):
        sha = hashlib.sha256()
        data = str(self.data).encode()
        sha.update(data)
        creator_id = str(self.creator_id).encode()
        sha.update(creator_id)
        timestamp = str(self.timestamp).encode()
        sha.update(timestamp)
        return sha.hexdigest()


# Write some markdown titles with streamlit on the app
st.markdown("# PyBlock")
st.markdown("## Store and hash data in a block")

# Receive input data from the user to put into the blockchain
input_data = st.text_area("Block Data")

# Create a button and add the a newly created Block object with all the date inside
if st.button("Add and Hash Block"):
    new_block = Block(data=input_data, creator_id=42, hash='')
    hashed_block = new_block.hash_block()
    st.write("New Block Fingerprint", hashed_block)
