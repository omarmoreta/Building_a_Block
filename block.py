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


# Write some markdown titles with streamlit on the app
st.markdown("# PyBlock")
st.markdown("## Store Data in a Block and hash data")

# Receive input data from the user to put into the blockchain
input_data = st.text_area("Block Data")

# Create a function to hash the input data


def hash_data(data):
    sha = hashlib.sha256()
    encoded_data = str(data).encode()
    sha.update(encoded_data)
    return sha.hexdigest()


# Create a button and add the a newly created Block object with all the date inside
if st.button("Add Block"):
    new_block = Block(
        data=input_data,
        creator_id=42,
        hash=hash_data(input_data)
    )
    st.write(new_block)
