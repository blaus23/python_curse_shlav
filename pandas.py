import pandas as pd

#1 - Noy
read_file = pd.read_excel ("Automobile_data.xlsx", sheet_name='in')
read_file.to_csv ("Automobile_data.csv", index = None, header=True)
df = pd.read_csv("Automobile_data.csv")
print(df.head(5))
print(df.tail(5))

#2 - Adi
if _name_ == '_main_':
    kk = pd.read_csv(r"C:\Users\טל המלך\PycharmProjects\panda\d.csv", na_values="?")
    kk.to_csv(r"C:\Users\טל המלך\PycharmProjects\panda\.csv")
    print(kk)

#3 - Noy
high_val = df.sort_values(by="price", ascending=False)
high_val = high_val[["company", "price"]]
print("Highest price:\n", high_val.head(1))

#4 - Noam
df = pd.read_csv(r"C:\Users\User\PycharmProjects\adi\Automobile_data.csv")
toy = df["company"].isin(["toyota"])
print(df[toy])

#5 = Maya
df = pd.read_csv(r'C:/Users/User/Automobile_data.csv')
count = df['company'].value_counts()
print(count)

#6 - Ofir
df = pd.read_csv('Automobile_data.csv')
df2 = df.groupby('company').max('price')
df2['company'] = df2.index
print(df2[['company', 'price']])

#7 - Amit
df = pd.read_csv('Automobile_data.csv')
print(df.groupby(['company'])['average-mileage'].agg(lambda x: x.unique().sum()/x.nunique()))

#8 - Ofir
df = pd.read_csv('Automobile_data.csv')
print(df.sort_values(by='price', ascending=False))

#9 - Yuval
GermanCars = {'Company': ['Ford', 'Mercedes', 'BMV', 'Audi'], 'Price': [23845, 171995, 135925 , 71400]}
japaneseCars = {'Company': ['Toyota', 'Honda', 'Nissan', 'Mitsubishi '], 'Price': [29995, 23600, 61500 , 58900]}
GermanCars = pd.DataFrame.from_dict(GermanCars)
japaneseCars = pd.DataFrame.from_dict(japaneseCars)
df_row = pd.concat([GermanCars, japaneseCars])
print(df_row)

#10 - Ofir
Car_Price = {'Company': ['Toyota', 'Honda', 'BMW', 'Audi'],
             'Price': [23845, 17995, 135925, 71400]}
Car_Horsepower = {'Company': ['Toyota', 'Honda', 'BMW', 'Audi'],
                  'Horsepower': [141, 80, 182, 160]}
df1 = pd.DataFrame(Car_Price)
df2 = pd.DataFrame(Car_Horsepower)
df3 = pd.merge(df1, df2, on='Company')
print(df3)



