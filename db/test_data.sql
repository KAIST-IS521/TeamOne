-- IMPORTANT! ALL EXISTING DATA ARE DELETED
DROP SCHEMA IF EXISTS `bankDB`;

source create_bankdb.sql
use bankDB;

INSERT INTO `auth_table` VALUES(
    'test',
    1
    );

INSERT INTO `user_table`
(`user_id`, `user_pw`,
 `email`, `mobile`, `balance`, `github_id`) VALUES(
    'test1',
    'test',
    'test@test.com',
    '01012341234',
    2000,
    'test'
), (
    'test2',
    'test',
    'test@test.com',
    '01012341234',
    1000,
    'test'
);

