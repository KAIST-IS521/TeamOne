use bankDB;

-- IMPORTANT! ALL EXISTING DATA ARE DELETED
DELETE FROM `auth_table`;
DELETE FROM `user_table`;

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
    5000,
    'test'
), (
    'test2',
    'test',
    'test@test.com',
    '01012341234',
    1000,
    'test'
);

