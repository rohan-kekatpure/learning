use aarwild_test;

drop table if exists jobs;

create table jobs(
    job_id char(16),
    name char(16)
);

drop table if exists jobs_data;

create table jobs_data (
    job_id char(16),
    data json
);

    
load data local infile '/Users/rohan/work/code/learning/mysql_/items.csv' into table jobs fields terminated by ',' lines terminated by '\n' ignore 1 lines;
load data local infile '/Users/rohan/work/code/learning/mysql_/items_json.csv' into table jobs_data fields terminated by '::' lines terminated by '\n';