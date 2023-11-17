#!/bin/bash
# bash script that deletes the qr images after they exceed their time
# of stay on the server
# use with cron tab enter crontab -e to add, enter crontab -l to list tasks

image_directory="~/Ezy_UrlShortner/v1/app/static/images/qr_images/"

# Find images older than 12 hours and delete them
find "$image_directory" -type f -name '*.png' -mmin +720 -delete

