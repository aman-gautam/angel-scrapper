import csv
import urllib2
import json
import time

with open('list.csv','w') as csvfile:
    list_writer = csv.writer(csvfile)
    
    for page in range(1,232):
        url = 'https://api.angel.co/1/jobs?page='+str(page)
        response=urllib2.urlopen(url)
        data = response.read()
        try:
            info = json.loads(data)
            #Now write to the csv file...
            for job in info['jobs']:
                try:
                    row = list()
                    row.append(job['id'])
                    row.append(job['title'])
                    row.append(job['description'])
                    row.append(job['created_at'])
                    row.append(job['updated_at'])
                    row.append(job['equity_cliff'])
                    row.append(job['equity_min'])
                    row.append(job['equity_max'])
                    row.append(job['equity_vest'])
                    row.append(job['currency_code'])
                    row.append(job['job_type'])
                    row.append(job['salary_min'])
                    row.append(job['salary_max'])
                    row.append(job['angellist_url'])
                    
                    try:
                        skills_filtered = filter(lambda x: x['tag_type']=='SkillTag',job['tags'])
                        row.append(reduce(lambda x,y: str(x)+','+str(y), map(lambda x: x['name'],skills_filtered)))
                    except:
                        row.append('')
                    try:
                        locations_filtered = filter(lambda x: x['tag_type']=='LocationTag', job['tags'])
                        row.append(reduce(lambda x,y: str(x)+','+str(y), map(lambda x: x['name'],locations_filtered)))
                    except:
                        row.append('')
                    try:
                        role_filtered = filter(lambda x:x['tag_type']=='RoleTag',job['tags'])
                        row.append(reduce(lambda x,y: str(x)+','+str(y), map(lambda x: x['name'],role_filtered)))
                    except:
                        row.append('')
                        
                    row.append(job['startup']['id'])
                    row.append(job['startup']['hidden'])
                    row.append(job['startup']['name'])
                    row.append(job['startup']['angellist_url'])
                    row.append(job['startup']['product_desc'])
                    row.append(job['startup']['high_concept'])
                    row.append(job['startup']['company_url'])
                    row.append(job['startup']['quality'])
                    row.append(job['startup']['follower_count'])
                except Exception,err1:
                    print repr(err1), ' Problem parsing the row ' , job
                finally:
                    print 'writing row = ', row
                    list_writer.writerow(row)
        except Exception,err2:
            print 'Some exception ',repr(err2)
        finally:
            print 'Done with page number ', page , '. Now taking a 3 sec break'

csvfile.close()