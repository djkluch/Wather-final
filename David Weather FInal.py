import json, requests

#START web address builder
class Weatherapi:
  def __init__(self,city="",w_url="",w_data=""):
    self.city = city
    self.w_url = w_url
    self.w_data = w_data
  
#set up the website call with inputed city.
  def city_get(self):
    print("What city would you like the tempature for?") 
    print("Or 'Q' to quit")
    city = input()
    #tests for number then sets to lower
    #may not need test for number though
    self.city = city.lower()
    return self

  def zip_get(self):
    print("What zip code would you like the tempature for?") 
    print("Or 'Q' to quit")
    zip = input()
    self.city = zip.lower()
    return self

      
  #For city name
  def url_make_city(self):
    #set basic url info
    #pulls from both City or Zip.
    base_url='https://api.openweathermap.org/data/2.5/weather?q='
    appid='dc9e99edbb4e1104a16a1ecde4f5f3d6'
    #combines to full website
    cityurl=f'{base_url}{self.city}&units=imperial&APPID={appid}'
    self.w_url = cityurl
    #print(self.w_url)
    #sends back full url
    return self

    #test if website is good
  def tester(self): 
    test = self.w_data
    try:
      #if an error shows up on the website it will show what you get
     test = test["main"]
    except:
      print('The website has returned an error: ', self.w_data['message'])
      print()
      main()
    else:
      print("Thank you!\n")
    
  
  def w_data_get(self):
  #get the requests from the website
    response = requests.get(self.w_url)
    new_data = response.json()
    self.w_data = new_data
    return self

  #show the json data from the website
  def print_wraw(self):
    data = json.dumps(self.w_data,indent=2)
    print(data)
    print()

  #if you need to print the url.
  def print_w_url(self):
    print(self.w_url)
    print()
  
  #show the temp for the user
  #may have to set out of Weatherapi?
  def temp_print(self):
    #print(self.w_data)
    temp = self.w_data['main']['temp']
    temp_max = self.w_data['main']['temp_max']
    temp = round(temp)
    temp_max = round(temp_max)
    print(f'The current temp is : {temp} F')
    print(f'The max temp is: {temp_max} F')
    print()  

#END Weatherapi

#START Loc_api
class Loc_api:
  def __init__(self,loc_url="",loc_data="",lat="",lon=""):
    self.loc_url = loc_url
    self.loc_data = loc_data
    self.lat = lat
    self.lon = lon
  
  #makes the URL
  def make_loc(self):
    print()
    base_url='http://api.openweathermap.org/geo/1.0/reverse?'
    appid='dc9e99edbb4e1104a16a1ecde4f5f3d6'
    lon = self.lon
    lat = self.lat
    self.loc_url = (f'{base_url}lat={lat}&lon={lon}&limit=5&appid={appid}')
    #print(self.loc_url)
    return self.loc_url

  
  def l_data_get(self):
    response = requests.get(self.loc_url)
    new_data = response.json()
    self.loc_data = new_data
    return self
  

  def print_l_raw(self):
    data = json.dumps(self.loc_data,indent=2)
    print(data)
    print()
  
  #print the location
  #move to new class of Loc_appi
  #or out of both?
  def print_loc(self):
    #print(self.loc_data)
    data = self.loc_data
    for city in data:
      city = city['name']
    for state in data:
      state = state['state']
    for country in data:
      country = country['country']
    print(f'For the city {city} in the state of {state}')
    print(f'located in {country}. The weather is as follows.\n')

#END Loc_Api

#Start data changes.
class Weather_change:
  def __init__(self,temp='',temp_min='',temp_max='',humidity='',wind_speed='',wind_deg=''):
    self.temp = temp
    self.temp_min = temp_min
    self.temp_max = temp_max
    self.humidity = humidity
    self.wind_speed = wind_speed
    self.wind_deg = wind_deg
    
    
  def __str__(self):
    return str(self.__class__) + ": " + str(self.__dict__)


  def update_raw(self,raw):
    print()
    self.temp = round(raw['main']['temp'])
    self.temp_max = round(raw['main']['temp_max'])
    self.temp_min = round(raw['main']['temp_min'])
    self.humidity = raw['main']['humidity']
    self.wind_speed = raw['wind']['speed']
    self.wind_deg = raw['wind']['deg']
  #check if data changed over right
    #data = self
    #print(data)

  def data_print(self):
    print(f'The current temp is : {self.temp} F')
    print(f'The min temp is: {self.temp_min} F')
    print(f'The max temp is: {self.temp_max} F')
    print(f'The humidity is: {self.humidity}%')
    if self.humidity <= 55:
      print('That is dry and comfortable.')
    elif self.humidity <= 65:
      print('It is sticky out right now.')
    else:
      print('There is a lot of moisture in the air.')
    print(f'The wind speed is: {self.wind_speed} knots')
    print(f'At {self.wind_deg} degrees from north.')
    print() 


#pick a number no text, could be used else where
def num_pick1_3():
  goto = ''
  while goto != '1' and goto != '2' and goto !='3':
    print('Please pick one of the following,')
    print('1 for city, 2 for zip, or 3 to quit.')
    goto = input()
  return goto


def main():
#sets the urlinput
  urlinput = Weatherapi()
  loc_input= Loc_api()
  correct_data = Weather_change()
  active = True
  #see what they want.
  while active:
    goto = num_pick1_3()
    if goto == '1':
      #will need to get city name input
      urlinput.city_get()     
    elif goto == '2':
      #will need to change to zip
      urlinput.zip_get()
    else:
      #close
      print('Thank you, have a great day.')
      break
      
    test = urlinput.city
    if test == "q":
      print('Thank you, have a great day.')
      break
    else:
      urlinput.url_make_city()
      urlinput.w_data_get()
      urlinput.tester()
      #correct_data.raw = urlinput.w_data
      correct_data.update_raw(urlinput.w_data)
      loc_input.lon = urlinput.w_data["coord"]["lon"]
      loc_input.lat = urlinput.w_data["coord"]["lat"]
      loc_input.make_loc()
      loc_input.l_data_get()
      loc_input.print_loc()
      print()
      correct_data.data_print()
      
main()