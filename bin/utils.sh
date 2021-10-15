#!/usr/bin/env bash

#gcloud projects create evekhm-testlab --name="$NAME" --folder=$FOLDER
#gcloud beta billing projects link evekhm-testlab --billing-account=$BILLING
#
#gcloud compute instances create $MACHINE --machine-type n1-standard-2 --zone $ZONE

gcloud projects create "$PROJECT_ID" --name="$PROJECT_NAME" --folder=$FOLDER
gcloud beta billing projects link "$PROJECT_ID" --billing-account="$BILLING"

gcloud compute instances create "$VM" --machine-type n1-standard-2

gcloud compute instances describe "$VM"

gcloud compute ssh "$VM"

#gcloud components list

https://source.cloud.google.com/evekhm-testlab/github_evekhm_gcp/+/main:bin/utils.sh

