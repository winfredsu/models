# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""A script to export the BERT core model as a TF-Hub SavedModel."""
from __future__ import absolute_import
from __future__ import division
# from __future__ import google_type_annotations
from __future__ import print_function

from absl import app
from absl import flags
import tensorflow as tf
from typing import Text

from official.nlp import bert_modeling

FLAGS = flags.FLAGS

flags.DEFINE_string("bert_config_file", None,
                    "Bert configuration file to define core bert layers.")
flags.DEFINE_string("model_checkpoint_path", None,
                    "File path to TF model checkpoint.")
flags.DEFINE_string("export_path", None,
                    "TF-Hub SavedModel destination path.")
flags.DEFINE_string("vocab_file", None,
                    "The vocabulary file that the BERT model was trained on.")


def create_bert_model(bert_config: bert_modeling.BertConfig):
  """Creates a BERT keras core model from BERT configuration.

  Args:
    bert_config: A BertConfig` to create the core model.

  Returns:
    A keras model.
  """
  # Adds input layers just as placeholders.
  input_word_ids = tf.keras.layers.Input(
      shape=(None,), dtype=tf.int32, name="input_word_ids")
  input_mask = tf.keras.layers.Input(
      shape=(None,), dtype=tf.int32, name="input_mask")
  input_type_ids = tf.keras.layers.Input(
      shape=(None,), dtype=tf.int32, name="input_type_ids")
  return bert_modeling.get_bert_model(
      input_word_ids,
      input_mask,
      input_type_ids,
      config=bert_config,
      name="bert_model",
      float_type=tf.float32)


def export_bert_tfhub(bert_config: bert_modeling.BertConfig,
                      model_checkpoint_path: Text, hub_destination: Text,
                      vocab_file: Text):
  """Restores a tf.keras.Model and saves for TF-Hub."""
  core_model = create_bert_model(bert_config)
  checkpoint = tf.train.Checkpoint(model=core_model)
  checkpoint.restore(model_checkpoint_path).assert_consumed()
  core_model.vocab_file = tf.saved_model.Asset(vocab_file)
  core_model.do_lower_case = tf.Variable("uncased" in vocab_file)
  core_model.save(hub_destination, include_optimizer=False, save_format="tf")


def main(_):
  assert tf.version.VERSION.startswith('2.')

  bert_config = bert_modeling.BertConfig.from_json_file(FLAGS.bert_config_file)
  export_bert_tfhub(bert_config, FLAGS.model_checkpoint_path,
                    FLAGS.export_path, FLAGS.vocab_file)


if __name__ == "__main__":
  app.run(main)
