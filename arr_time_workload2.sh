./bin/run-example --conf spark.scheduler.mode=FAIR --conf spark.useSLAQ=false mllib.Mixed1secExample &> mix1secnoslaq.log
./bin/run-example --conf spark.scheduler.mode=FAIR --conf spark.useSLAQ=true mllib.Mixed1secExample &> mix1secslaq.log

./bin/run-example --conf spark.scheduler.mode=FAIR --conf spark.useSLAQ=false mllib.MixedhsecExample &> mixhsecnoslaq.log
./bin/run-example --conf spark.scheduler.mode=FAIR --conf spark.useSLAQ=true mllib.MixedhsecExample &> mixhsecslaq.log
