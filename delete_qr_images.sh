#!/bin/bash
# bash script that deletes the qr images after they exceed their time
# of stay on the server

image_directory="~/Ezy_UrlShortner/app/v1/static/images/qr_images/"

# Find images older than 12 hours and delete them
find "$image_directory" -type f -name '*.png' -mmin +720 -delete

