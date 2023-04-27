import mysql.connector


mydb = mysql.connector.connect(
 host="PLACE DATABASE SERVER HERE",
 user="PLACE DATABASE USER HERE",
 password="PLACE DATABASE PASSWORD HERE",
 database="PLACE DATABASE NAME HERE"
)

def regesiterUser(Date_of_Birth, email, gender, password, username, features):
    passed = True
    mycursor = mydb.cursor()
    try:
        sql = """
        INSERT INTO User_buyer (Date_of_Birth, email, gender, password, username)
        VALUES ("{0}","{1}","{2}","{3}","{4}");
        """.format(Date_of_Birth, email, gender, password, username)
        mycursor.execute(sql)
        for car in features:
            sql = """
            INSERT INTO User_buyer_intCars (email, car_make, car_model, car_year)
            VALUES ("{0}","{1}","{2}","{3}");
            """.format(email, car[0], car[1], car[2])
            mycursor.execute(sql)
        mydb.commit()
        sql = """
        select * from User_buyer_intCars;
        """
        mycursor.execute(sql)
        result = mycursor.fetchall()
        for r in result:
            print(r)
        sql = """
                select * from User_buyer;
                """
        mycursor.execute(sql)
        result = mycursor.fetchall()
        for r in result:
            print(r)
    except Exception as e:
        passed = False
        print("Duplicate: ", e)
    return passed

def UserPurchase(AdId, email, priceBought, rating, review):
    mycursor = mydb.cursor()
    passed = True
    try:
        sql = """
        INSERT INTO Purchase (AdId, email, priceBought, rating, review)
        VALUES ("{0}","{1}","{2}","{3}","{4}");
        """.format(AdId, email, priceBought, rating, review)
        mycursor.execute(sql)
        mydb.commit()
    except Exception as e:
        passed = False
        print("Car in advertisment Already Sold ")
    return passed

def viewReview(AdId):
    mycursor = mydb.cursor()
    sql = """
    select review from Purchase where AdId = {0};
    """.format(AdId)
    print(sql)
    mycursor.execute(sql)
    review = mycursor.fetchall()
    return review

def viewRating(phone):
        mycursor = mydb.cursor()
        sql = """
            SELECT AVG(P.rating) AS aggregated_rating 
            FROM Purchase AS P 
            INNER JOIN CarAdvert AS C 
            ON P.AdId = C.AdId 
            WHERE C.Phone = '{0}'
        """.format(phone)
        mycursor.execute(sql)
        rating = mycursor.fetchall()
        return rating[0]

def showAdsAvgPrice(body_type, Make, Car_year, location):
    location = "%" + location + "%"
    mycursor = mydb.cursor()
    sql = """
    select car_model, avg(priceListed) from CarAdvert Where car_make = "{0}" AND body_type = "{1}" AND car_year like "{2}"AND location like "{3}" group by car_model;
    """.format(Make, body_type, Car_year, location)
    print(sql)
    mycursor.execute(sql)
    lines = list()
    for (Model, Avg) in mycursor:
        lines.append([Model, Avg])
    return lines

def showAllads(body_type, Make, Car_year, location):
    location = "%" + location + "%"
    mycursor = mydb.cursor()
    sql = """
       select * from CarAdvert Where car_make = "{0}" AND body_type = "{1}" AND car_year like "{2}"AND location like "{3}";
       """.format(Make, body_type, Car_year, location)
    print(sql)
    mycursor.execute(sql)
    lines = list()
    for row in mycursor:
        print(row)
        lines.append(row)
    return lines

def filterFeatures(features, low, high, location):
    mycursor = mydb.cursor()
    location = "%"+location+"%"
    sql = """
    SELECT ad.AdId, ad.car_make, ad.car_model, ad.priceListed
    FROM CarAdvert ad
    INNER JOIN CarADvert_features cf ON ad.AdId = cf.AdId
    WHERE ad.location like '{0}'
    AND ad.priceListed >= {1} AND ad.priceListed <= {2}
    AND cf.Feauture IN ({3})
    GROUP BY ad.AdID
    HAVING COUNT(DISTINCT cf.Feauture) = {4}
    """.format(location, low, high, ", ".join(["'{}'".format(f) for f in features]), len(features))
    print(sql)
    mycursor.execute(sql)
    lines = list()
    for (id, make, model, price) in mycursor:
        lines.append([id, make, model, price])
    return lines

def Top5Location(make, model):
    mycursor = mydb.cursor()
    sql = """
    SELECT location, count(AdId) as amount, avg(priceListed) as average_price
    from CarAdvert
    where car_make = "{0}" AND car_model = "{1}" AND location like "%cairo%"
    group by location
    order by amount desc, average_price desc
    limit 5
    """.format(make, model)
    print(sql)
    mycursor.execute(sql)
    lines = list()
    for (location, amount, avgPrice) in mycursor:
        lines.append([location, amount, avgPrice])
    return lines

def checkUser(email, password):
    DBpassword = None
    mycursor = mydb.cursor()
    sql = """
        select password from User_buyer where email = "{0}";
        """.format(email)
    print(sql)
    mycursor.execute(sql)
    for (word) in mycursor:
        DBpassword = word[0]
    if DBpassword == None:
        return False
    if DBpassword == password:
        return True
    else:
        return False


def SellerInventory(phone):
    mycursor = mydb.cursor()
    sql = """
    SELECT AdId, car_make, car_model, car_year from CarAdvert where Phone = {0};
    """.format(phone)
    print(sql)
    mycursor.execute(sql)
    lines = list()
    for (AdId, make, model, year) in mycursor:
        lines.append([AdId, make, model, year])
    return lines

def top5amount(low, high):
    mycursor = mydb.cursor()
    sql = """
        SELECT car_make, car_model, COUNT(AdId) as inventory_count, AVG(priceListed) as average_price 
        FROM CarAdvert
        WHERE car_year BETWEEN {0} AND {1} 
        GROUP BY car_make, car_model 
        ORDER BY inventory_count DESC 
        LIMIT 5;
            """.format(low,high)
    print(sql)
    mycursor.execute(sql)
    lines = list()
    for (make, model, inventory, averagePrice) in mycursor:
        lines.append([make, model, inventory, averagePrice])
    return lines

def top5sellers():
    mycursor = mydb.cursor()
    sql = """
        SELECT S.Phone, S.Fname, S.Lname, sum(amount) AS Amount, AVG(price_year)
        FROM (
            SELECT phone, Car_year, count(AdId) as amount,AVG(priceListed) AS price_year
            FROM CarAdvert
            GROUP BY phone, Car_year
        ) AS sub
        INNER JOIN Seller AS S ON sub.phone = S.phone
        GROUP BY S.Phone, S.Fname, S.Lname
        ORDER BY Amount DESC
        LIMIT 5;
            """
    print(sql)
    mycursor.execute(sql)
    lines = list()
    for (Phone, Fname, Lname, Amount, Average) in mycursor:
        lines.append([Phone, Fname, Lname, Amount, Average])
    print
    return lines

