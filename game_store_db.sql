INSERT INTO store_employee (id, first_name, last_name, email) VALUES
(1, 'John', 'Doe', 'JohnDoe3433@gmail.com'),
(2, 'Jane', 'Smith', 'JaneSmith@gmail.com'),
(3, 'Jim', 'Brown', 'JimBrown@gmail.com'),
(4, 'Eve', 'Evans', 'EveEvans4085@gmail.com'),
(5, 'Hank', 'Harris', 'HankHarris@gmail.com'),
(6, 'Noah', 'Nelson', 'NoahNelson@gmail.com');

INSERT INTO store_products (id, title, description, price, discount, stock_quantity, release_date, added_by_employee_id) VALUES
(1, 'Super Mario 64 - Nintendo 64','On a bright, sunny day in the Mushroom Kingdom, Mario goes to visit the princess but finds her castle eerily empty. Leaping through pictures hanging from the walls, he enters 15 magical worlds in a quest to collect the 120 Power Stars pilfered by evil Bowser and save the day. The game''s vast worlds teem with daunting obstacle courses, hidden items, puzzles and more than 30 types of enemies. Take advantage of Mario''s large selection of moves, including running, jumping, swimming, stomping, punching, and even backward somersaulting! Special caps give him short-lived powers, including the ability to fly. Super Mario 64 features unmatched camera control that makes adventuring in its 3D world a snap, even for newcomers.',37.99,0,64,'1996-09-27', 1),
(2, 'Wii Sports - Nintendo Wii','Wii Sports on Nintendo Wii offers five distinct sports experiences, each using the Wii Remote to provide a natural, intuitive and realistic feel. Players can use their own Mii caricatures in the game and play them against their friends'' Miis for a more personalized experience. As players improve, their Miis'' skill levels will increase, so that they can see exactly how much better they''ve become.',34.99, 10,15,'2006-12-08',2),
(3, 'New Nintendo 3DS XL Handheld Console - Black','The New Nintendo 3DS XL - Black is a cutting-edge handheld gaming device that offers an immersive gaming experience with its face tracking 3D technology. This feature allows the device to adjust the 3D display based on the user''s viewing angle, providing a more realistic and captivating gameplay. Additionally, the C Stick provides enhanced control and precision, allowing gamers to navigate through games effortlessly. With built-in amiibo support, players can unlock exclusive content and features by simply tapping their amiibo figures on the device. The New 3DS XL also boasts a larger screen size compared to its predecessor, offering a more immersive visual experience. With its sleek and stylish design, this handheld console is perfect for gaming on the go. Whether you''re a casual gamer or a hardcore enthusiast, the New Nintendo 3DS XL is sure to deliver hours of entertainment and excitement.',279.99,0,5,'2014-08-11',2);

INSERT INTO store_category (id, name) VALUES
(1, 'Game'),
(2, 'Console');

INSERT INTO store_products_product_category (id, products_id, category_id) VALUES
(1, 1, 1),
(2, 2, 1),
(3, 3, 2);
