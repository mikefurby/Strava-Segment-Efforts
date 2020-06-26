#!/bin/bash
#Version 20.1

awsdst="s3://vscc-challenges.cc/apps/"
aws s3 cp ~/apps/clubsetup.sh $awsdst --region eu-west-1
aws s3 cp ~/apps/awsupload.sh $awsdst --region eu-west-1
aws s3 cp ~/apps/newbuildmemberlist.py $awsdst --region eu-west-1
aws s3 cp ~/apps/divisions.py $awsdst --region eu-west-1
aws s3 cp ~/apps/divisionsgrimp.py $awsdst --region eu-west-1
aws s3 cp ~/apps/finalisehtml.sh $awsdst --region eu-west-1
aws s3 cp ~/apps/finalisehtmlgrimp.sh $awsdst --region eu-west-1
aws s3 cp ~/apps/leagues.py $awsdst --region eu-west-1
aws s3 cp ~/apps/leaguesgrimp.py $awsdst --region eu-west-1
aws s3 cp ~/apps/segfiles.py $awsdst --region eu-west-1
aws s3 cp ~/apps/segmentefforts.py $awsdst --region eu-west-1
aws s3 cp ~/apps/segmentparams.py $awsdst --region eu-west-1
aws s3 cp ~/apps/vs3linit.py $awsdst --region eu-west-1

#THE END
