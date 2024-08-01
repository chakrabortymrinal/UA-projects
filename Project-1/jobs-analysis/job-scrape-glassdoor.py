import csv
from jobspy import scrape_jobs

# List of countries to scrape jobs from
countries = [
    'argentina', 'australia', 'austria', 'bahrain', 'belgium', 'brazil', 'canada', 
    'chile', 'china', 'colombia', 'costa rica', 'czech republic', 'czechia', 'denmark', 
    'ecuador', 'egypt', 'finland', 'france', 'germany', 'greece', 'hong kong', 
    'hungary', 'india', 'indonesia', 'ireland', 'israel', 'italy', 'japan', 'kuwait', 
    'luxembourg', 'malaysia', 'mexico', 'morocco', 'netherlands', 'new zealand', 
    'nigeria', 'norway', 'oman', 'pakistan', 'panama', 'peru', 'philippines', 'poland', 
    'portugal', 'qatar', 'romania', 'saudi arabia', 'singapore', 'south africa', 
    'south korea', 'spain', 'sweden', 'switzerland', 'taiwan', 'thailand', 'turkey', 
    'ukraine', 'united arab emirates', 'uk', 'united kingdom', 'usa', 'us', 'united states', 
    'uruguay', 'venezuela', 'vietnam', 'usa/ca', 'worldwide'
]

site_name = 'glassdoor'
search_term = "machine learning"
results_wanted = 500000

for country in countries:
    try:
        jobs = scrape_jobs(
            site_name=["glassdoor"],
            search_term=search_term,
            location=country,
            results_wanted=results_wanted,
            country_indeed=country  # only needed for indeed / glassdoor
        )
        print(f"Found {len(jobs)} jobs in {country}")
        
        # Save the jobs to a CSV file
        filename = f"job-{site_name}-{country}.csv"
        jobs.to_csv(filename, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
        print(f"Saved jobs in {country} to {filename}")
    except Exception as e:
        print(f"Failed to scrape jobs for {country}: {str(e)}")
