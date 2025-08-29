SELECT DISTINCT field_districtID AS "Student Id",
  field_firstName AS "Student First Name", 
  field_middleName AS "Student Middle Name",
  field_lastName AS "Student Last Name", 
  '' AS "Student Generation", 
  '' AS "FoodIntolerance",
  field_birthdate AS "Birthdate",
  field_gender AS "Student Gender",
  CASE
  	WHEN field_race = 'Asian' THEN 3
  	WHEN field_race = 'White' THEN 6
  	WHEN field_race = 'Black' THEN 4
  	WHEN field_race = 'Native Am.' THEN 2
  	WHEN field_race = 'Hawaiian' THEN 5
  	ELSE ''
  END AS  "Federal Race Code",
  CASE
  	WHEN field_ethnicity = 'Hispanic' THEN 'Y'
  	WHEN field_ethnicity = 'Non-Hispanic' THEN 'N'
  	ELSE ''
  END AS "Hispanic/Latino Ethnicity",
  field_graduationYear + field_gradeLevel - 12 AS "Current School Year", 
  field_siteShortName AS "Current Building",
   field_gradeLevel AS "Student Grade", 
   '' AS "Student Homeroom Primary", 
   CASE
   	WHEN field_address2 IS NULL THEN field_address1
   	WHEN field_address2 IS NOT NULL THEN CONCAT(field_address1, ', ', field_address2)
   END AS 'Street Addr Line & Apt - Physical',
   field_addressCity AS "City - Physical", 
   field_addressState AS "State - Physical",
   field_addressZip AS "Zip - Physical", 
   CASE
   	WHEN field_address2 IS NULL THEN field_address1
   	WHEN field_address2 IS NOT NULL THEN CONCAT(field_address1, ', ', field_address2)
   END AS 'Street Addr Line & Apt - Mailing', 
   field_addressCity AS "City - Mailing", 
   field_addressState AS "State - Mailing",
   field_addressZip "Zip - Mailing",
   field_guardian1FirstName AS "First Name - Guardian",
   field_guardian1MiddleName AS "Middle Name - Guardian", 
   field_guardian1LastName AS "Last Name - Guardian",
   field_guardian1MobilePhone AS "Mobile Phone",
   field_guardian1HomePhone AS "Home Phone",
   field_guardian1WorkPhone AS "Work Phone",
   field_email1 AS "Email - Guardian",
   'Other Family Relative' AS "Relation Name - Guardian",
   'English' AS "Student Language",
   CONCAT('HH-', field_siteShortName, '-', field_districtID) AS "HHID",
   CASE 
    	WHEN CURDATE() > '2025-08-25' THEN DATE_FORMAT(CURDATE(), '%%m/%%d/%%Y')
    	ELSE '08/25/2025'
	END AS `Enrollment Date`
FROM dscdata.destinystudentsCharter
WHERE field_siteShortName = 295 OR
  field_siteShortName = 543 OR
  field_siteShortName = 575;						
