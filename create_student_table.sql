CREATE TABLE `administrators` (
  `EMAIL` varchar(200) NOT NULL,
  `PASSWORD` varchar(200) NOT NULL,
  PRIMARY KEY (`EMAIL`)
);

CREATE INDEX idx_email ON `administrators` (`EMAIL`);

CREATE TABLE courses (
  `COURSEID` varchar(200) NOT NULL,
  `COURSE_NAME` varchar(200) NOT NULL,
  PRIMARY KEY (`COURSEID`)
);

INSERT INTO courses (COURSEID, COURSE_NAME) VALUES
('C001', 'Mathematics'),
('C002', 'Physics'),
('C003', 'Computer Science'),
('C004', 'English'),
('C005', 'History');


CREATE TABLE `students` (
    `STUDID` varchar(200) NOT NULL,
    `FNAME` varchar(200) NOT NULL,
    `LNAME` varchar(200) NOT NULL,
    `ADDRESS` varchar(200) NOT NULL,
    `PHONE` varchar(200) NOT NULL,
    `GENDER` varchar(10) NOT NULL,  -- Adding a gender column
     PRIMARY KEY (`STUDID`)
    );

-- Add a foreign key reference in the students table to associate a course with a student
ALTER TABLE students ADD COLUMN COURSEID varchar(200);
ALTER TABLE students ADD FOREIGN KEY (COURSEID) REFERENCES courses(COURSEID);


INSERT INTO students (STUDID, FNAME, LNAME, ADDRESS, PHONE, GENDER, COURSEID) VALUES
    ('S001', 'Alice', 'Johnson', '123 Main St', '555-1234', 'Female', 'C001'),
    ('S002', 'Bob', 'Smith', '456 Oak St', '555-5678', 'Male', 'C002'),
    ('S003', 'Charlie', 'Williams', '789 Pine St', '555-9012', 'Male', 'C003'),
    ('S004', 'David', 'Brown', '987 Elm St', '555-3456', 'Male', 'C004'),
    ('S005', 'Eva', 'Miller', '654 Birch St', '555-7890', 'Female', 'C005'),
    ('S006', 'Frank', 'Taylor', '321 Cedar St', '555-2345', 'Male', 'C001'),
    ('S007', 'Grace', 'Anderson', '876 Maple St', '555-6789', 'Female', 'C002'),
    ('S008', 'Henry', 'Martinez', '543 Walnut St', '555-0123', 'Male', 'C003'),
    ('S009', 'Ivy', 'Clark', '210 Pineapple St', '555-4567', 'Female', 'C004'),
    ('S010', 'Jack', 'White', '135 Orange St', '555-8901', 'Male', 'C005'),
    ('S011', 'Karen', 'Davis', '975 Mango St', '555-2345', 'Female', 'C001'), 
    ('S012', 'Larry', 'Garcia', '753 Banana St', '555-6789', 'Male', 'C002'), 
    ('S013', 'Mia', 'Thomas', '246 Strawberry St', '555-0123', 'Female', 'C003'),
    ('S014', 'Nathan', 'Hill', '864 Blueberry St', '555-4567', 'Male', 'C004'),
    ('S015', 'Olivia', 'Young', '321 Raspberry St', '555-8901', 'Female', 'C005'),
    ('S016', 'Paul', 'Brown', '987 Lemon St', '555-2345', 'Male', 'C001'),
    ('S017', 'Quincy', 'Gomez', '654 Grape St', '555-6789', 'Male', 'C002'),
    ('S018', 'Rachel', 'Turner', '987 Cherry St', '555-0123', 'Female', 'C003'),
    ('S019', 'Samuel', 'Cooper', '210 Peach St', '555-4567', 'Male', 'C004'), 
    ('S020', 'Tina', 'Flores', '753 Plum St', '555-8901', 'Female', 'C005');


-- Assign roles to users
INSERT INTO user_roles (`EMAIL`, `ROLE`) VALUES ('user@localhost', 'user');


-- Create user 'user' identified by 'user_password'
CREATE USER 'user'@'localhost' IDENTIFIED BY 'user_password';

-- Grant SELECT privileges on students and courses tables to user role
GRANT SELECT ON students_db.students TO 'user'@'localhost';
GRANT SELECT ON students_db.courses TO 'user'@'localhost';