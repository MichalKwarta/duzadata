add JAR /usr/lib/hive/lib/hive-hcatalog-core.jar;



CREATE EXTERNAL TABLE IF NOT EXISTS collisions_ext(
    street STRING,
    zipcode STRING,
    person_type STRING,
    damage_type STRING,
    count INT)
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY '\t'
stored as textfile
location '${hiveconf:input_dir3}';


select * from collisions_ext;


CREATE EXTERNAL TABLE IF NOT EXISTS zipcode_ext(
    zipcode STRING,
    borough STRING)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
location '${hiveconf:input_dir4}'
tblproperties("skip.header.line.count"="1");



CREATE EXTERNAL TABLE IF NOT EXISTS manhattan_street_ext(
    street STRING,
    person_type STRING,
    killed INT,
    injured INT)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.JsonSerDe'
STORED AS TEXTFILE
  location '${hiveconf:output_dir6}';

INSERT OVERWRITE TABLE manhattan_street_ext
SELECT street, person_type, killed, injured
FROM (
    SELECT street, person_type, SUM(killed) AS killed, SUM(injured) AS injured,
        RANK() OVER (PARTITION BY person_type ORDER BY SUM(killed) + SUM(injured) DESC) AS rank_in_person_type
    FROM (SELECT zipcode, street, person_type,
                 CASE WHEN damage_type = 'INJURED' THEN count ELSE 0 END injured,
                 CASE WHEN damage_type = 'KILLED' THEN count ELSE 0 END killed
          FROM collisions_ext) c
    JOIN zipcode_ext z ON (z.zipcode = c.zipcode)
    WHERE z.borough = 'MANHATTAN'
    GROUP BY c.street, c.person_type
) r
WHERE r.rank_in_person_type <= 3;