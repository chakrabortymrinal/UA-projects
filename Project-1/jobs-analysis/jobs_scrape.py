import csv
from jobspy import scrape_jobs
# ValueError: Invalid country string: 'in'. Valid countries are: argentina, australia, austria, bahrain, belgium, brazil, canada, chile, china, colombia, costa rica, czech republic,czechia, 
# denmark, ecuador, egypt, finland, france, germany, greece, hong kong, hungary, india, indonesia, ireland, israel, italy, japan, kuwait, luxembourg, malaysia, mexico, morocco, netherlands, 
# new zealand, nigeria, norway, oman, pakistan, panama, peru, philippines, poland, portugal, qatar, romania, saudi arabia, singapore, south africa, south korea, spain, sweden, switzerland, 
# taiwan, thailand, turkey, ukraine, united arab emirates, uk,united kingdom, usa,us,united states, uruguay, venezuela, vietnam, usa/ca, worldwide
site_name='glassdoor'
ct='uk'
jobs = scrape_jobs(
    # site_name=["indeed","linkedin", "zip_recruiter", "glassdoor"],
    site_name=["glassdoor"],
    search_term="machine learning",
    location="united kingdom",
    results_wanted=500000,
    # hours_old=72, # (only Linkedin/Indeed is hour specific, others round up to days old)
    country_indeed='united kingdom',  # only needed for indeed / glassdoor
    
    # linkedin_fetch_description=True # get full description , direct job url , company industry and job level (seniority level) for linkedin (slower)
    # proxies=["208.195.175.46:65095", "208.195.175.45:65095", "localhost"],
    
)
print(f"Found {len(jobs)} jobs")
print(jobs.head())
jobs.to_csv(f"jobs-{site_name}-{ct}.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False) # to_excel