def read(con):
    query = 'select * from t_player;'
    try:
        cursor = con.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
    except Exception as e:
        print(e)
    finally :
        if con:
            cursor.close()    
        return data    
 
def getByName(name,con):
    query = 'select * from t_player where name like %s;'
    try:
        cursor = con.cursor()
        cursor.execute(query,(name,))
        row = cursor.fetchone()
        cursor.close()
        return row
    except Exception as e:
        print(e)
    finally :
        if con:
            cursor.close()    

#data must be list of tuple
def load(data,con):
    query = 'insert into t_player(name,score) values(%s,%s);'
    try:
        cursor = con.cursor()
        cursor.executemany(query,data)
        con.commit()
    except Exception as e:
        print(e)
    finally:
        if con:
            cursor.close()

def create(player,con):
    query = 'insert into t_player(name,score) values(%s,%s);'
    try:
        cursor = con.cursor()
        cursor.execute(query,player)
        con.commit()
    except Exception as e:
        print(e)
    finally:
        if con:
            cursor.close()    

def delete(player,con):
    query = 'delete from t_player where name like %s;'
    try:
        cursor = con.cursor()
        cursor.execute(query,(player,))
        con.commit()
    except Exception as e:
        print(e)
    finally:
        if con:
            cursor.close()

def update(name,score,con):
    query = 'update t_player set score=%s where name like %s;'
    try:
        cursor = con.cursor()
        cursor.execute(query,(str(score),name))
        con.commit()
    except Exception as e:
        print(e)
    finally:
        if con:
            cursor.close()