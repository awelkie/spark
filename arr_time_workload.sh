./bin/run-example --conf spark.scheduler.mode=FAIR --conf spark.useSLAQ=false mllib.Mixed2secExample &> mix2secnoslaq.log
./bin/run-example --conf spark.scheduler.mode=FAIR --conf spark.useSLAQ=true mllib.Mixed2secExample &> mix2secslaq.log
./bin/run-example --conf spark.scheduler.mode=FAIR --conf spark.useSLAQ=false mllib.Mixed4secExample &> mix4secnoslaq.log
./bin/run-example --conf spark.scheduler.mode=FAIR --conf spark.useSLAQ=true mllib.Mixed4secExample &> mix4secslaq.log
./bin/run-example --conf spark.scheduler.mode=FAIR --conf spark.useSLAQ=false mllib.Mixed6secExample &> mix6secnoslaq.log
./bin/run-example --conf spark.scheduler.mode=FAIR --conf spark.useSLAQ=true mllib.Mixed6secExample &> mix6secslaq.log
./bin/run-example --conf spark.scheduler.mode=FAIR --conf spark.useSLAQ=false mllib.Mixed8secExample &> mix8secnoslaq.log
./bin/run-example --conf spark.scheduler.mode=FAIR --conf spark.useSLAQ=true mllib.Mixed8secExample &> mix8secslaq.log
./bin/run-example --conf spark.scheduler.mode=FAIR --conf spark.useSLAQ=false mllib.Mixed10secExample &> mix10secnoslaq.log
./bin/run-example --conf spark.scheduler.mode=FAIR --conf spark.useSLAQ=true mllib.Mixed10secExample &> mix10secnoslaq.log
