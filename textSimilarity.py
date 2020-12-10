

#@title Load the Universal Sentence Encoder's TF Hub module

from absl import logging

import tensorflow as tf

import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    print("check")
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

module_url = "https://tfhub.dev/google/universal-sentence-encoder/4" #@param ["https://tfhub.dev/google/universal-sentence-encoder/4", "https://tfhub.dev/google/universal-sentence-encoder-large/5"]
model = hub.load(module_url)
print ("module %s loaded" % module_url)

def embed(input):
  return model(input)
