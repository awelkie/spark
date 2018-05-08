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
import org.apache.spark.mllib.clustering.{KMeans, KMeansModel}
import org.apache.spark.mllib.linalg.Vectors
// $example off$

object KMeansSlaqExample {

  def main(args: Array[String]) {

    val conf = new SparkConf().setAppName("KMeansSlaqExample")
    val sc = new SparkContext(conf)

    sc.SLAQnewPool()

    // Load and parse the data
    val data = sc.textFile("data/mllib/kmeans_data.txt")
    val parsedData = data.map(s => Vectors.dense(s.split(' ').map(_.toDouble))).cache()
    val numClusters = 20
    val numIterations = 1000

    val numJobs = 100
    val threads = (0 to numJobs).map {_ =>
      new Thread {
        sc.SLAQnewPool()

        override def run(): Unit = {
          KMeans.train(parsedData, numClusters, numIterations)
        }
      }
    }

    for (t <- threads) {
      Thread.sleep(5 * 1000)
      t.start()
    }

    for (t <- threads) {
      t.join()
    }

    sc.stop()
  }
}
// scalastyle:on println
