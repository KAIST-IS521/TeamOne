use bankDB;

-- IMPORTANT! ALL EXISTING DATA ARE DELETED
DELETE FROM `auth_table`;
DELETE FROM `user_table`;

INSERT INTO `auth_table` VALUES(
    'test',
    'DUMMY KEY', 
    1
    );

INSERT INTO `user_table` VALUES(
    'test1',
    0,
    'test',
    'test@test.com',
    '01012341234',
    5000,
    'test'
), (
    'test2',
    1,
    'test',
    'test@test.com',
    '01012341234',
    1000,
    'test'
);

