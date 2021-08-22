from bs4 import BeautifulSoup
import requests
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request

app = Flask(__name__)
@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")

@app.route('/hello', methods=['POST'])
def hello():
    meal1 = request.form['meal1']
    meal2 = request.form['meal2']
    meal3 = request.form['meal3']
    meal4 = request.form['meal4']
    meal5 = request.form['meal5']
    email = request.form['email']
    f = open("recipes.txt", "w")
    f.write(meal1 + ","+ meal2 + ","+ meal3 + ","+ meal4 + ","+ meal5)
    f.close()
    f2 = open("email.txt", "w")
    f2.write(email + ",")
    f2.close()
    return "Thank you! Please check your email for your lovely meal plan!"

if __name__ == '__main__':
    app.run(debug=True)


def generateGroceryList(recipes):
    item = []
    item_list = []
    grocery_list = []
    #When user inputs 0, program exits
    for recipe_website in recipes:
        try:
            #Read data off of website
            
            html_text=requests.get(recipe_website).text
            soup = BeautifulSoup(html_text,"lxml")
            #Getting list of ingredients
            ingredient_list= soup.find_all('span',class_="ingredients-item-name")
            for i in range(len(ingredient_list)):
                ingredient_list[i]=ingredient_list[i].text
            counter=0
            for i in range(len(ingredient_list)):
                ingredient_list_temp=ingredient_list[i].split()
                counter=0
                for j in range(len(ingredient_list_temp)):
                    #if no instances of cups etc, it will do full ingredient
                    if ingredient_list_temp[j]=="cup" or ingredient_list_temp[j]=="cups" or ingredient_list_temp[j]=="teaspoon" or ingredient_list_temp[j]=="teaspoons" or ingredient_list_temp[j]=="tablespoon" or ingredient_list_temp[j]=="tablespoons":
                        item.append(ingredient_list[i].split()[j+1:])
                        counter+=1
                if counter==0:
                    item.append(ingredient_list[i].split()[1:])
    
            #converting list of strings(item) into 1 string each
            for i in range(len(item)):
                item_word = ""
                for j in range(len(item[i])):
                    item_word=item_word + " "+item[i][j]
                item_list.append(item_word)
    
            for i in range(len(item_list)):
                grocery_list.append(item_list[i])

        except:
            print("error: try recipe from allrecipes or check url")
    grocery_list=list(dict.fromkeys(grocery_list))
    grocery_list=sorted(grocery_list)
    
    return grocery_list

def extractWebsites(txt_file):
    with open(txt_file) as recipes:
        recipes=recipes.read().split(',')
    return recipes

def mail_list(list,reciever):
    sender_email='stopshopandrollinc@gmail.com'
    sender_pass='StopShop&Roll'
    #with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    server=smtplib.SMTP('smtp.gmail.com',587)
    #encrypt traffic
    server.starttls()
    server.ehlo()

    server.login(sender_email,sender_pass)
    subject="Stop,Shop and Roll: Your Personalized Grocery Shopping list!"
    body = ""
    for i in list:
        body += f'{str(i)}/n'
    msg=EmailMessage()
    msg['Subject']=subject
    msg['From']=sender_email
    msg['To']=reciever
    msg.set_content(body)

    server.send_message(msg)


for i in generateGroceryList(extractWebsites("recipes.txt")):
    print(i)
mail_list(generateGroceryList(extractWebsites("recipes.txt")), extractWebsites("email.txt"))






