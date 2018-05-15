/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

// scalastyle:off println
package org.apache.spark.examples.mllib

import org.apache.spark.{SparkConf, SparkContext}
// $example on$
import org.apache.spark.mllib.classification.{LogisticRegressionModel, LogisticRegressionWithLBFGS, SVMModel, SVMWithSGD}
import org.apache.spark.mllib.clustering.{KMeans, KMeansModel}
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.mllib.regression.LabeledPoint
import org.apache.spark.mllib.util.MLUtils
// $example off$

object Mixed1secExample {

  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName("MixedExample")
    val sc = new SparkContext(conf)

    // $example on$
    // Load training data in LIBSVM format.
    // val data = MLUtils.loadLibSVMFile(sc, "data/mllib/sample_libsvm_data.txt")
    val dataLR = MLUtils.loadLibSVMFile(sc, "data/mllib/mnist.scale")
    // Split data into training (60%) and test (40%).
    val splitsLR = dataLR.randomSplit(Array(0.95, 0.05), seed = 11L)
    val trainingLR = splitsLR(0).cache()
//    val test = splits(1).cache()

    val dataKM = sc.textFile("data/mllib/kmeans_data.txt")
    val parsedDataMK = dataKM.map(s => Vectors.dense(s.split(' ').map(_.toDouble))).cache()

    val dataSVM = MLUtils.loadLibSVMFile(sc, "data/mllib/real-sim_post")
    val splitsSVM = dataSVM.randomSplit(Array(0.9, 0.1), seed = 11L)
    val trainingSVM = splitsSVM(0).cache()

    // Run training algorithm to build the model
    val numClusters = 20
    val numJobs = 160

    val threads = (0 to numJobs).map {i =>
        new Thread {
            override def run(): Unit = {
                sc.SLAQnewPool()
                val rd = scala.util.Random
                val op = rd.nextInt(4)
                if (op >=3) {
                    val model = new LogisticRegressionWithLBFGS()
                      .setNumClasses(10)
                      .run(trainingLR)
                } else if (op >=2) {
                    val model = SVMWithSGD.train(trainingSVM, 1000)
                } else {
                    KMeans.train(parsedDataMK, 20, 1000)
                }
            }
        }
    }

    for (t <- threads) {
        Thread.sleep(1000*1)
        t.start()
    }

    for (t <- threads) {
        t.join()
    }

//    val model = new LogisticRegressionWithLBFGS()
//      .setNumClasses(10)
//      .run(training)

    // Compute raw scores on the test set.
//    val predictionAndLabels = test.map { case LabeledPoint(label, features) =>
//      val prediction = model.predict(features)
//      (prediction, label)
//    }

    // Get evaluation metrics.
//    val metrics = new MulticlassMetrics(predictionAndLabels)
//    val accuracy = metrics.accuracy
//    println(s"Accuracy = $accuracy")

    // Save and load model
//    model.save(sc, "target/tmp/scalaLogisticRegressionWithLBFGSModel")
//    val sameModel = LogisticRegressionModel.load(sc,
//      "target/tmp/scalaLogisticRegressionWithLBFGSModel")
    // $example off$

    sc.stop()
  }
}

