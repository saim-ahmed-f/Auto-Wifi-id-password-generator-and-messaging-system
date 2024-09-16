import pyodbc

def extarct_data(query , format = None , col = None  , action = None):    
    main_data = [
        # ('201'),
        # ('201'),
        # ('401')
    ]

    try:
        
        conn = pyodbc.connect(
            #'DSN=testing_connect;UID=Tameem;PWD=;'
            'DSN=python_connector;UID=JNRPMS;PWD=Jnr@Pms23;'
        ) 

        # Cursor
        cursor = conn.cursor()

        # Query
        cursor.execute(query)

        # Fetch Data
        if format != None:
            main_data = {}
            check = []

            for i in cursor.fetchall():
                if i[0] not in check:
                    check.append(i[0])
                    main_data[str(i[0])] = [[i[1] , i[2] , i[3]]]
                else:
                    main_data[str(i[0])].append([i[1] , i[2] , i[3]])

        else:
            main_data = {}
            check = []
            for k in  cursor.fetchall():
                if k[0] not in check:
                    main_data[str(k[0])] = str(k[1])
                    check.append(k[0]) # -- UPDATED

        conn.close()

    except Exception as error:
        print(error)
        exit()

    
    # main_data = {
    #     '201' : '12345',
    #     '301' : '01234',
        
    # }

    if len(main_data) != 0:
        return main_data
    else:
        return False
    


def phone_no_check(phone): # -- UPDATED
    phone = str(phone).strip()
    phone_len = len(phone)
    if phone_len == 13:
        return phone[3:]
    elif phone_len == 12:
        return phone[2:]
    elif phone_len == 11:
        return phone[1:]
    else:
        return phone 


def extarct_data_from_sql_for_phone_check(query , action = None , room = None , phone_nos = None):    
    data = [
        # ('201' , 'Miss Inab Hashmi' , '7247336070'),
        # ('201' , 'Mr Saim Ahmed' , '7247336071'),
        # ('201' , 'Miss Daniya' , '9713674707')
    ]
    if action == "room":
        query += str(room)
        query += " ;"

        #data = [('9893211055', ''), (' ', ''), ('9893211055', '')]

    elif action == "phone":
        all_phone_main = ""
        for index , phone_value   in enumerate(phone_nos):
            all_phone_main += "\'" + str(phone_value) + "\'"
            if len(phone_nos) != index+1:
                all_phone_main += ","

        query += "\'" + str(room) + "\'"
        query += " and [FAXNUB] NOT IN ("
        query += all_phone_main
        query += ");"
        
        #data = [('7247336081', 'MR Ahmed')]
    
    try:
        
        conn = pyodbc.connect(
            #'DSN=testing_connect;UID=Tameem;PWD=;'
            'DSN=python_connector;UID=JNRPMS;PWD=Jnr@Pms23;'
        ) 

        # Cursor
        cursor = conn.cursor()

        # Query
        cursor.execute(query)

        # Fetch Data
        for j in cursor.fetchall():
            data.append(j)

        print(cursor.fetchall())

        if len(data) != 0:
            check = {}
            for i in data:
                if len(str(i[0]).strip()) != 0:
                    phone_no = phone_no_check(str(i[0]))
                    if len(phone_no) != 0:
                        check[str(phone_no)] = str(i[1])
            return check
        else:
            return {}
        
        

    except Exception as error:
        print(error , "from sql")
        exit()
    finally:
        conn.close()

    # if action == "room":
    #     check = {}
    #     for i in data:
    #         if i not in check.keys():
    #             check[str(i[0])] = 
    #     return  check
    # elif action == "phone":
    
    
    # if len(data) != 0:
    #     check = {}
    #     for i in data:
    #         if len(str(i[0]).strip()) != 0:
    #             check[str(i[0])] = str(i[1])
    #     return check
    # else:
    #     return {}



if __name__ == "__main__":
    print (extarct_data("sd"))

