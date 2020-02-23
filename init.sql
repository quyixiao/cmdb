-- 表1 虚拟表host，有2个字段hostname、ip
INSERT INTO `schema` (name) VALUES('host');
INSERT INTO `field` (name, schema_id) VALUES ('hostname', 1);
INSERT INTO `field` (name, schema_id) VALUES ('ip', 1);
-- 表2 虚拟表ippool，有1个字段ip
INSERT INTO `schema` (name) VALUES('ippool');
INSERT INTO `field` (name, schema_id) VALUES ('ip', 2);
-- host表添加记录
INSERT INTO entity (`key`, schema_id) VALUES ('5846d1499dd544198475a9d517766494', 1);
INSERT INTO `value`(entity_id, field_id, `value`) VALUES(1, 1, 'webserver');



INSERT INTO `value`(entity_id, field_id, `value`) VALUES(1, 2, '192.168.1.10');
INSERT INTO entity (`key`, schema_id) values ('0f51405a04344f0e9f11109895ab2f19', 1);
INSERT INTO `value`(entity_id, field_id, `value`) VALUES(2, 1, 'DBserver');
INSERT INTO `value`(entity_id, field_id, `value`) VALUES(2, 2, '192.168.1.20');
INSERT INTO entity (`key`, schema_id) VALUES ('587723df88a54b2e9f449888d75f50de', 1);
INSERT INTO `value` (entity_id, field_id, `value`) VALUES(3, 1, 'DNS Server');
INSERT INTO `value` (entity_id, field_id, `value`) VALUES(3, 2, '172.16.100.1');
-- ip表添加记录
INSERT INTO entity (`key`, schema_id) VALUES('3dea5d2e39eb47b5a5b95cee6fc64f8d', 2);
INSERT INTO entity (`key`, schema_id) VALUES('6bbd0d91e6cf44cba7e71207ddaa06d6', 2);
INSERT INTO entity (`key`, schema_id) VALUES('fc377c758e5a463cb246ff693ab11434', 2);

INSERT INTO `value` (entity_id, field_id, `value`) VALUES(4, 3, '192.168.1.10');
INSERT INTO `value`(entity_id, field_id, `value`) VALUES(5, 3, '192.168.1.20');
INSERT INTO `value`(entity_id, field_id, `value`) VALUES(6, 3, '192.168.1.30');


-- 查询
SELECT
`schema`.id AS sid,
`schema`.`name` AS sname,
entity.id AS eid,
entity.`key`,
field.id AS fid,
field.`name` AS fname,
`value`.id,
`value`.`value`
FROM
`value`
INNER JOIN entity ON `value`.entity_id = entity.id AND entity.deleted = FALSE INNER JOIN `schema` ON entity.schema_id = `schema`.id AND `schema`.deleted = FALSE INNER JOIN field ON `value`.field_id = field.id AND field.deleted = FALSE
WHERE `value`.deleted = FALSE