from flask import Flask, render_template, request, session, url_for, redirect
import sqlReader as sq
app = Flask(__name__, template_folder="/Users/ahmedmoamen/Desktop/ahmed/school/2023 spring/Databases/Car Sale Database/project_milestone3/templates")
app.secret_key = 'project2'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        dob = request.form['dob']
        gender = request.form['gender']
        make = request.form.getlist('make[]')
        model = request.form.getlist('model[]')
        year = request.form.getlist('year[]')

        cars = []
        for i in range(len(make)):
            car = [make[i], model[i], year[i]]
            cars.append(car)
        print(username, password, email, dob, gender, cars)
        if sq.regesiterUser(dob, email, gender, password, username, cars):
            return render_template('index.html')
        else:
            return render_template('register.html')

@app.route('/Sale_page')
def Sale_page():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    if sq.checkUser(email, password):
        session['email'] = email
        return render_template('sale.html')
    else:
        return render_template('login.html')


@app.route('/add_sale',  methods=['GET', 'POST'])
def add_sale():
    AdId = request.form['ad_id']
    PriceBought = request.form['price_bought']
    rating = request.form['rating']
    review = request.form['review']
    email = session.get('email')

    if sq.UserPurchase(AdId, email, PriceBought, rating, review):
        return render_template('index.html')
    else:
        return render_template('sale.html')

@app.route('/view_reviews')
def view_reviews():
    return render_template('viewReview.html')

@app.route('/Search01', methods=['GET', 'POST'])
def Search01():
    AdId = request.form.get("ad_id")
    result = sq.viewReview(AdId)
    if result:
        review = result[0]
        return render_template('viewReview.html', review= review, ADID= AdId)
    else:
        return render_template('viewReview.html')

@app.route('/view_rating')
def view_rating():
    return render_template('view _aggregated_rating.html')

@app.route('/Search00', methods=['GET', 'POST'])
def Search00():
    phone = request.form.get("phone_number")
    print(phone)
    result = sq.viewRating(phone)
    rating = result[0]
    return render_template('view _aggregated_rating.html', rating= str(rating)+"/5")


@app.route('/show_ads')
def show_ads():
    return render_template('show_all_ads.html')

@app.route('/Search0', methods=['GET', 'POST'])
def Search0():
    Make = request.form.get('Make')
    Year = request.form.get('Year')
    Location = request.form.get('Location')
    BodyType = request.form.get('BodyType')
    table1 = sq.showAllads(BodyType,Make,Year,Location)
    table2 = sq.showAdsAvgPrice(BodyType,Make,Year,Location)
    return render_template('show_all_ads.html', table1= table1, table2= table2)

@app.route('/show_used_cars')
def show_used_cars():
    return render_template('filterFeatures.html')
@app.route('/Search1', methods=['GET', 'POST'])
def Search1():
    features = request.form.getlist('Features[]')
    min_price = request.form.get('min-price')
    max_price = request.form.get('max-price')
    location = request.form.get('location')
    results = sq.filterFeatures(features,min_price,max_price, location)
    return render_template('filterFeatures.html', results= results)

@app.route('/top_areas')
def top_areas():
    return render_template('top5location.html')
@app.route('/Search2', methods=['GET', 'POST'])
def Search2():
    make = request.form.get('make')
    model = request.form.get('model')
    results = sq.Top5Location(make, model)
    print(results)
    return render_template('top5location.html', results= results)

@app.route('/top_sellers')
def top_sellers():
    results = sq.top5sellers()
    return render_template('top5Sellers.html', results= results)

@app.route('/show_properties')
def show_properties():
    return render_template("sellerInventory.html")

@app.route('/Search3', methods=['GET', 'POST'])
def Search3():
    phone = request.form.get('Phone')
    results = sq.SellerInventory(phone)
    return render_template('sellerInventory.html', results= results)

@app.route('/top_cars')
def top_cars():
    return render_template('top5amount.html')

@app.route('/Search4', methods=['GET', 'POST'])
def Search4():
    min = request.form.get('LowYear')
    max = request.form.get('HighYear')
    results = sq.top5amount(min, max)
    return render_template('top5amount.html', results= results)


