#!/bin/bash
club=$1

#UPLOAD
awsdst="s3://www.vscc-challenges.cc/$club/"
aws s3 cp ~/$club/html/index.html $awsdst --region eu-west-1
aws s3 cp ~/$club/html/current.html $awsdst --region eu-west-1
aws s3 cp ~/$club/html/seasontable.html $awsdst --region eu-west-1
aws s3 cp ~/$club/html/liveleague1.html $awsdst --region eu-west-1
aws s3 cp ~/$club/html/liveleague2.html $awsdst --region eu-west-1
aws s3 cp ~/$club/html/liveleague3.html $awsdst --region eu-west-1
aws s3 cp ~/$club/html/liveleague4.html $awsdst --region eu-west-1
aws s3 cp ~/$club/html/liveleague5.html $awsdst --region eu-west-1
aws s3 cp ~/$club/html/liveleague6.html $awsdst --region eu-west-1
aws s3 cp ~/$club/html/liveleague7.html $awsdst --region eu-west-1
aws s3 cp ~/$club/html/liveleague8.html $awsdst --region eu-west-1
aws s3 cp ~/$club/html/liveleague9.html $awsdst --region eu-west-1
aws s3 cp ~/$club/html/liveleague10.html $awsdst --region eu-west-1
aws s3 cp ~/$club/html/liveleague11.html $awsdst --region eu-west-1
aws s3 cp ~/$club/html/matrix11.html $awsdst --region eu-west-1
aws s3 cp ~/$club/get$club.sh $awsdst --region eu-west-1
aws s3 cp ~/$club/archive/seasontable20201.html $awsdst --region eu-west-1

#THE END
