#!/usr/bin/python3
#-*- coding: utf-8 -*-
import pymysql

def insertPeopleTraffic( peopleTrafficHit ):
    connect = pymysql.connect( host="poc.ci9niqaqsefm.us-east-1.rds.amazonaws.com", user= "jump", passwd="jump1234", db="poc" )
    cursorQuery = connect.cursor()

    sql = "INSERT INTO people_traffic (people_traffic_hit) VALUES ('" + str( peopleTrafficHit ) + "')"
    cursorQuery.execute( sql )
    id = cursorQuery.lastrowid

    if( id ):
        print('Incluido com sucesso')

    connect.commit()
    connect.close()
