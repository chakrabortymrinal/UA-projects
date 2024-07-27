#!/bin/bash

# to run the script copy and `chmod +x <file name>`
# create a out folder where all files will be copied in

# file was not found , downloading previous days , I did try to use TZ and set it to US but we can't be 
# sure where the servers are located and when do their job kick in to create the files for the present day   
previous_day_date=$(date -u -d "yesterday" +"%m_%d_%Y")

# Define the download links as in https://developer.themoviedb.org/docs/daily-id-exports
urls=(
    "http://files.tmdb.org/p/exports/movie_ids_${previous_day_date}.json.gz"
    "http://files.tmdb.org/p/exports/tv_series_ids_${previous_day_date}.json.gz"
    "http://files.tmdb.org/p/exports/person_ids_${previous_day_date}.json.gz"
    "http://files.tmdb.org/p/exports/collection_ids_${previous_day_date}.json.gz"
    "http://files.tmdb.org/p/exports/tv_network_ids_${previous_day_date}.json.gz"
    "http://files.tmdb.org/p/exports/keyword_ids_${previous_day_date}.json.gz"
    "http://files.tmdb.org/p/exports/production_company_ids_${previous_day_date}.json.gz"
)

# iterate , and use the file name  https://www.geeksforgeeks.org/basename-command-in-linux-with-examples/
for url in "${urls[@]}"; do
    # Extract the file name from the URL
    output_file=$(basename "$url")

    # Download the file
    wget --no-check-certificate -O "./out/$output_file" "$url"

    # check if files exsists
    cd out
    if [[ $? -ne 0 ]]; then
        echo "Failed to download $url"
    else
        echo "Successfully downloaded $output_file"

        gunzip "$output_file"

        # unzip checks
        if [[ $? -ne 0 ]]; then
            echo "Failed to unzip $output_file"
        else
            echo "Successfully unzipped $output_file"
        fi
    fi
    # remove all the zipped files
    rm -rf *.json.gz
    cd ..
done
