USE catalog;
drop table if exists progress;
CREATE TABLE if not exists progress (
	ID INT PRIMARY KEY auto_increment,
    card_id int, 
	DESCRIPTION VARCHAR(1024), 
	DATETIME DATETIME default current_timestamp on update current_timestamp,
    foreign key(card_id) references card(id)	
);

insert into progress ( card_id, DESCRIPTION) select ID, DESCRIPTION from card;
