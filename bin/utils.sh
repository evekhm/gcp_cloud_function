#!/usr/bin/env bash
export FOLDER=261046259366
export NAME='Test Lab'
export BILLING='01382E-07CCE9-615E10'
gcloud projects create evekhm-testlab --name="$NAME" --folder=$FOLDER
gcloud beta billing projects link evekhm-testlab --billing-account=$BILLING