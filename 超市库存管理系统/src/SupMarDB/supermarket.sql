-- 1. 删除表
DROP TABLE IF EXISTS purchase;
DROP TABLE IF EXISTS sale;
DROP TABLE IF EXISTS staff;
DROP TABLE IF EXISTS client;
DROP TABLE IF EXISTS goods;

-- 2. 创建客户表
CREATE TABLE client (
    client_id CHAR(10) PRIMARY KEY NOT NULL,
    client_name VARCHAR(20) NOT NULL,
    phone_number VARCHAR(11) UNIQUE,
    address VARCHAR(10)
);

-- 3. 创建员工表
CREATE TABLE staff (
    staff_id CHAR(10) PRIMARY KEY NOT NULL,
    staff_name VARCHAR(20) NOT NULL,
    department VARCHAR(10) NOT NULL,
    salary DECIMAL(8,2) NOT NULL ,
    phone_number VARCHAR(11) UNIQUE,
    CHECK (salary>=0)
);

-- 4. 创建商品表
CREATE TABLE goods (
    goods_id CHAR(10) PRIMARY KEY NOT NULL,
    goods_name VARCHAR(20) NOT NULL,
    goods_num INT DEFAULT 0,
    CHECK (goods_num >= 0)
);

-- 5. 创建进货表
CREATE TABLE purchase (
    purchase_id CHAR(10) PRIMARY KEY NOT NULL,
    goods_id CHAR(10) NOT NULL ,
    staff_id CHAR(10) NOT NULL ,
    purchase_price DECIMAL(6,2) NOT NULL ,
    purchase_num INT NOT NULL ,
    purchase_amount DECIMAL(8,2) NOT NULL ,
    purchase_date DATE NOT NULL ,
    CONSTRAINT fk_goods1 FOREIGN KEY (goods_id) REFERENCES goods(goods_id),
    CONSTRAINT fk_staff FOREIGN KEY (staff_id) REFERENCES staff(staff_id),
    CHECK (purchase_price >= 0),
    CHECK (purchase_num >= 0),
    CHECK (purchase_amount = purchase_price * purchase_num)
);

-- 6. 创建销售表
CREATE TABLE sale (
    sale_id CHAR(10) PRIMARY KEY NOT NULL,
    client_id CHAR(10),
    goods_id CHAR(10),
    sale_price DECIMAL(6,2),
    sale_num INT,
    sale_amount DECIMAL(8,2),
    sale_date DATE,
#     profit DECIMAL(8,2),
    CONSTRAINT fk_client FOREIGN KEY (client_id) REFERENCES client(client_id),
    CONSTRAINT fk_goods2 FOREIGN KEY (goods_id) REFERENCES goods(goods_id),
    CHECK (sale_price >= 0),
    CHECK (sale_num >= 0),
    CHECK (sale_amount = sale_price * sale_num)
);

-- 触发器
-- 2. 工作部门必须是 sale or purchase
-- 限制插入
DROP TRIGGER IF EXISTS enforce_department_insert_constraint;
DELIMITER //
CREATE TRIGGER enforce_department_insert_constraint
BEFORE INSERT ON staff
FOR EACH ROW
BEGIN
IF NEW.department != 'purchase' AND NEW.department != 'sale' THEN
SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insert Department must be "purchase" or "sale"';
END IF;
END //
DELIMITER ;

-- 限制更新
DROP TRIGGER IF EXISTS enforce_department_update_constraint;
DELIMITER //
CREATE TRIGGER enforce_department_update_constraint
BEFORE UPDATE ON staff
FOR EACH ROW
BEGIN
    IF NEW.department != 'purchase' AND NEW.department != 'sale' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Update Department must be "purchase" or "sale"';
    END IF;
END //
DELIMITER ;


-- 3. 插入或更新时自动给计算进货的总金额=进货单价*进货数量
DROP TRIGGER IF EXISTS calculate_insert_purchase_amount;
DELIMITER //
CREATE TRIGGER calculate_insert_purchase_amount
BEFORE INSERT ON purchase
FOR EACH ROW
BEGIN
    SET NEW.purchase_amount = NEW.purchase_price * NEW.purchase_num;
END //

DROP TRIGGER IF EXISTS calculate_update_purchase_amount;
CREATE TRIGGER calculate_update_purchase_amount
BEFORE UPDATE ON purchase
FOR EACH ROW
BEGIN
    SET NEW.purchase_amount = NEW.purchase_price * NEW.purchase_num;
END //
DELIMITER ;

-- 4. 插入或更新时自动给计算销售的总金额=销售单价*销售数量
DROP TRIGGER IF EXISTS calculate_insert_sale_amount;
DELIMITER //
CREATE TRIGGER calculate_insert_sale_amount
BEFORE INSERT ON sale
FOR EACH ROW
BEGIN
    SET NEW.sale_amount = NEW.sale_price * NEW.sale_num;
END //

DROP TRIGGER IF EXISTS calculate_update_sale_amount;
CREATE TRIGGER calculate_update_sale_amount
BEFORE UPDATE ON sale
FOR EACH ROW
BEGIN
    SET NEW.sale_amount = NEW.sale_price * NEW.sale_num;
END //
DELIMITER ;

-- 插入或更新时自动更新库存信息

DELIMITER //
DROP TRIGGER IF EXISTS update_goods_num_purchase_insert;
-- 创建更新进货表触发器
CREATE TRIGGER update_goods_num_purchase_insert
AFTER INSERT ON purchase
FOR EACH ROW
BEGIN
    UPDATE goods
    SET goods_num = goods_num + NEW.purchase_num
    WHERE goods_id = NEW.goods_id;
END //

-- 创建更新销售表触发器
DROP TRIGGER IF EXISTS update_goods_num_sale_insert;
CREATE TRIGGER update_goods_num_sale_insert
AFTER INSERT ON sale
FOR EACH ROW
BEGIN
    UPDATE goods
    SET goods_num = goods_num - NEW.sale_num
    WHERE goods_id = NEW.goods_id;
END //

-- 创建更新进货表触发器
DROP TRIGGER IF EXISTS update_goods_num_purchase_update;
CREATE TRIGGER update_goods_num_purchase_update
AFTER UPDATE ON purchase
FOR EACH ROW
BEGIN
    UPDATE goods
    SET goods_num = goods_num + (NEW.purchase_num - OLD.purchase_num)
    WHERE goods_id = NEW.goods_id;
END //

-- 创建更新销售表触发器
DROP TRIGGER IF EXISTS update_goods_num_sale_update;
CREATE TRIGGER update_goods_num_sale_update
AFTER UPDATE ON sale
FOR EACH ROW
BEGIN
    UPDATE goods
    SET goods_num = goods_num - (NEW.sale_num - OLD.sale_num)
    WHERE goods_id = NEW.goods_id;
END //

DELIMITER ;



-- 7. 添加测试数据
INSERT INTO client (client_id, client_name, phone_number, address) VALUES ('c1', '张三','15023456789', '重庆市');
INSERT INTO client (client_id, client_name, phone_number, address) VALUES ('c2', '李四', '13987654321', '上海市');
INSERT INTO client (client_id, client_name, phone_number, address) VALUES ('c3', '王五', '13212345678', '广州市');
INSERT INTO client (client_id, client_name, phone_number, address) VALUES ('c4', '赵六', '18665432109', '深圳市');
INSERT INTO client (client_id, client_name, phone_number, address) VALUES ('c5', '孙七', '13598761234', '成都市');

INSERT INTO staff (staff_id, staff_name, department, salary, phone_number) VALUES ('s1', '王五', 'purchase', 6000.00, '13987654321');
INSERT INTO staff (staff_id, staff_name, department, salary, phone_number) VALUES ('s2', '赵六', 'sale', 5500.00, '13212345678');
INSERT INTO staff (staff_id, staff_name, department, salary, phone_number) VALUES ('s3', '孙七', 'purchase', 6200.00, '18665432109');
INSERT INTO staff (staff_id, staff_name, department, salary, phone_number) VALUES ('s4', '周八', 'purchase', 5800.00, '13598761234');
INSERT INTO staff (staff_id, staff_name, department, salary, phone_number) VALUES ('s5', '钱九', 'sale', 5900.00, '15023456789');
-- 检查约束，部门只能为sale或purchase
# INSERT INTO staff (staff_id, staff_name, department, salary, phone_number) VALUES ('006', '钱九', '1', 5900.00, '15023456789');
# UPDATE staff set department='sale' where staff_id='002';

INSERT INTO goods (goods_id, goods_name) VALUES ('g1', '香蕉');
INSERT INTO goods (goods_id, goods_name) VALUES ('g2', '西瓜');
INSERT INTO goods (goods_id, goods_name) VALUES ('g3', '橙子');
INSERT INTO goods (goods_id, goods_name) VALUES ('g4', '菠萝');
INSERT INTO goods (goods_id, goods_name) VALUES ('g5', '草莓');

INSERT INTO purchase (purchase_id, goods_id, staff_id, purchase_price, purchase_num, purchase_amount, purchase_date) VALUES ('p1', 'g1', 's1', 5.00, 200, 1000.00, '2023-03-01');
INSERT INTO purchase (purchase_id, goods_id, staff_id, purchase_price, purchase_num, purchase_amount, purchase_date) VALUES ('p2', 'g2', 's2', 8.00, 150, 1200.00, '2023-04-01');
INSERT INTO purchase (purchase_id, goods_id, staff_id, purchase_price, purchase_num, purchase_amount, purchase_date) VALUES ('p3', 'g3', 's3', 6.50, 180, 1170.00, '2023-05-01');
INSERT INTO purchase (purchase_id, goods_id, staff_id, purchase_price, purchase_num, purchase_amount, purchase_date) VALUES ('p4', 'g4', 's4', 12.00, 120, 1440.00, '2023-06-01');
INSERT INTO purchase (purchase_id, goods_id, staff_id, purchase_price, purchase_num, purchase_amount, purchase_date) VALUES ('p5', 'g5', 's5', 15.00, 100, 1500.00, '2023-07-01');
-- 检查约束
-- 即使不输入purchase_amount或者输入错了也会纠正
# INSERT INTO purchase (purchase_id, goods_id, staff_id, purchase_price, purchase_num, purchase_date) VALUES ('p6', 'g5', 's4', 16.00, 110, '2023-08-01');
# INSERT INTO purchase (purchase_id, goods_id, staff_id, purchase_price, purchase_num, purchase_amount, purchase_date) VALUES ('p7', 'g5', 's4', 16.00, 100, 1500.00, '2023-09-01');


INSERT INTO sale (sale_id, client_id, goods_id, sale_price, sale_num, sale_amount, sale_date) VALUES ('sa1', 'c1', 'g1', 7.00, 100, 700.00, '2023-04-01');
INSERT INTO sale (sale_id, client_id, goods_id, sale_price, sale_num, sale_amount, sale_date) VALUES ('sa2', 'c2', 'g2', 10.00, 80, 800.00, '2023-05-01');
INSERT INTO sale (sale_id, client_id, goods_id, sale_price, sale_num, sale_amount, sale_date) VALUES ('sa3', 'c3', 'g3', 9.00, 100, 900.00, '2023-06-01');
INSERT INTO sale (sale_id, client_id, goods_id, sale_price, sale_num, sale_amount, sale_date) VALUES ('sa4', 'c4', 'g4', 14.00, 90, 1260.00, '2023-07-01');
INSERT INTO sale (sale_id, client_id, goods_id, sale_price, sale_num, sale_amount, sale_date) VALUES ('sa5', 'c5', 'g5', 18.00, 70, 1260.00, '2023-08-01');
-- 检查约束
-- 即使不输入sale_amount或者输入错了也会纠正
# INSERT INTO sale (sale_id, client_id, goods_id, sale_price, sale_num, sale_date) VALUES ('007', '128', '006', 18.00, 100, '2023-08-01');
# INSERT INTO sale (sale_id, client_id, goods_id, sale_price, sale_num, sale_amount, sale_date) VALUES ('008', '128', '006', 18.00, 100, 1260.00, '2023-09-01');

-- 检查约束插入或更新时自动更新库存信息
update sale set sale_num = 110.0 where sale_id='sa1';
update purchase set purchase_num = 210.0 where purchase_id='p1';

select * from sale;