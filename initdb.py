#coding: utf-8
import pymysql

def initdb():
	db = pymysql.connect("localhost","root","toor")
	cursor = db.cursor()
	cursor.execute("create database if not exists flask")
	db.commit()
	db.close()
	db = pymysql.connect("localhost","root","toor","flask")
	cursor = db.cursor()

	# mysql预处理语句
	sql1 = "create table if not exists users(username varchar(20) not null,passwd varchar(100),money int)" 
	sql2 = "create table if not exists goods(gname varchar(20) not null,glink varchar(300),gmoney int)" 

	cursor.execute(sql1)
	cursor.execute(sql2)

	db.commit()
	db.close()
	
if __name__ == '__main__':
	initdb()
