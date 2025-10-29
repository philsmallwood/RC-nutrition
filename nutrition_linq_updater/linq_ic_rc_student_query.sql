SELECT DISTINCT s.studentNumber AS "Student Id",
  s.firstName AS "Student First Name", 
  s.middleName AS "Student Middle Name",
  s.lastName AS "Student Last Name", 
  s.suffix AS "Student Generation", 
  '' AS "FoodIntolerance",
  FORMAT(s.birthdate, 'MM/dd/yyyy') AS "Birthdate",
  s.gender AS "Student Gender",
  s.raceEthnicity AS "Federal Race Code",
  s.hispanicEthnicity AS "Hispanic/Latino Ethnicity", 
  s.endYear AS "Current School Year", 
  '320' + SUBSTRING(
        s.calendarName,
        CHARINDEX('(', s.calendarName) + 1,
        CHARINDEX(')', s.calendarName) - CHARINDEX('(', s.calendarName) - 1
   ) AS "Current Building",
   s.grade AS "Student Grade", 
   rm.name AS "Student Homeroom Primary", 
   c.addressLine1 AS 'Street Addr Line & Apt - Physical', 
   c.city AS "City - Physical", 
   c.state AS "State - Physical",
   c.zip AS "Zip - Physical", 
   c.addressLine1 AS 'Street Addr Line & Apt - Mailing', 
   c.city AS "City - Mailing", 
   c.state AS "State - Mailing",
   c.zip "Zip - Mailing",
   c.firstName AS "First Name - Guardian",
   c.middleName AS "Middle Name - Guardian", 
   c.lastName AS "Last Name - Guardian",
   c.cellPhone AS "Mobile Phone",
   c.householdPhone AS "Home Phone",
   c.workPhone AS "Work Phone",
   c.email AS "Email - Guardian",
   c.relationship AS "Relation Name - Guardian",
   CASE 
     WHEN s.homePrimaryLanguage = 'spa' THEN 'Spanish' 
     ELSE 'English'
   END AS "Student Language",
   'HH' + CAST(c.householdID AS VARCHAR(100)) AS "HHID",
   CASE 
        WHEN GETDATE() > '2025-08-25' THEN FORMAT(GETDATE(), 'MM/dd/yyyy')
        ELSE '08/25/2025'
    END AS "Enrollment Date"
FROM student s
LEFT JOIN v_CensusContactSummary c ON c.personGUID = s.personGUID AND 
  c.seq = 1 AND
  c.guardian = 1 AND
  c.relatedBy = 'household'
LEFT JOIN (
    SELECT r.personID, rm.name
    FROM Roster r
    INNER JOIN v_ClassSection cs 
        ON cs.sectionID = r.sectionID AND cs.courseNumber = '8889'
    INNER JOIN Room rm 
        ON rm.roomID = cs.roomID
WHERE (r.endDate >= GETDATE() OR r.endDate IS NULL) AND (r.startDate <= GETDATE() OR r.startDate IS NOT NULL)  AND cs.teacherPersonID IS NOT NULL) rm ON rm.personID = s.personID
WHERE s.activeYear = 1 AND
  s.startDate > s.calendarStart - 1 AND
  (s.endDate >= GETDATE() OR s.endDate IS NULL) AND
  s.studentNumber IS NOT NULL AND
  s.calendarName NOT LIKE '%888%' AND
  s.calendarName NOT LIKE '%530%';