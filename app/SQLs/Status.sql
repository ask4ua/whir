select count(*) "Messages Total "from messages;

select count(*) "Message Not yet" from messages left join words on words.word_id=messages.message_id where words.word_id is Null and messages.inprogress_flag=FALSE;

select count(*) "Messages In Progress" from messages where messages.inprogress_flag=TRUE;

select count(*) "Total Words" from words;
select sum(wordsinword.count) "Total wordsinword" from wordsinword;

--update messages set inprogress_flag=False;