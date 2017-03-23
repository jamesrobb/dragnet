#!/usr/bin/python3

import argparse

import tensorflow as tf

from dragnet_nn.data_loader import data_loader
from dragnet_nn.dragnet_nn import *

import hashlib
import json


def main(matrices_file, labels_file):
    test_loader = data_loader(matrices_file)
    test_matrices, empty_labels = test_loader.all_data()

    #print(hashlib.md5(json.dumps(test_matrices, sort_keys=True).encode("utf-8")).hexdigest())

    dimension = 900
    evidence_classes = 76
    output_labels = [[x for x in range(0, evidence_classes)]] * len(test_matrices)

    # print(test_matrices)
    # print(output_labels)

    x = tf.placeholder(tf.float32, [None, dimension])

    W_conv1 = weight_variable([5, 5, 1, 32])
    b_conv1 = bias_variable([32])

    x_image = tf.reshape(x, [-1,30,30,1])

    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

    W_conv2 = weight_variable([5, 5, 32, 64])
    b_conv2 = bias_variable([64])

    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)

    W_fc1 = weight_variable([8 * 8 * 64, 1024])
    b_fc1 = bias_variable([1024])

    h_pool2_flat = tf.reshape(h_pool2, [-1, 8*8*64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

    keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    W_fc2 = weight_variable([1024, evidence_classes])
    b_fc2 = bias_variable([evidence_classes])

    y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2

    y_ = tf.placeholder(tf.float32, [None, evidence_classes])
    #cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))

    #correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
    #accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    saver = tf.train.Saver()
    sess = tf.InteractiveSession()
    sess.run(tf.global_variables_initializer())

    saver = tf.train.import_meta_graph(DRAGNET_NN_BRAIN_LOCATION + "dragnet_brain.ckpt.meta")
    saver.restore(sess, tf.train.latest_checkpoint(DRAGNET_NN_BRAIN_LOCATION))

    prediction = tf.argmax(y_conv,1)
    prediction_result = sess.run(prediction, feed_dict={x: test_matrices, keep_prob: 1.0, y_:output_labels})

    sess.close()

    print(prediction_result)

    output_fh = open(labels_file, 'w')
    for i in prediction_result:
        output_fh.write(str(i) + "\n")

    output_fh.close()
    #probabilities = tf.nn.softmax(y_conv)
    #print(sess.run(probabilities, feed_dict={x: test_matrices, keep_prob: 0.5}))
    #print("test accuracy %g"%accuracy.eval(feed_dict={x: test_matrices, y_: test_labels, keep_prob: 1.0}))
    


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("matrices_file", help="source of matrices")
    parser.add_argument("labels_file", help="destination of labels")
    args = parser.parse_args()

    main(args.matrices_file, args.labels_file)