import pandas as pd 
def get_back_camera_mp_sum(back_camera_str):
    mega_pixels_sum = 0
    
    if back_camera_str is None or back_camera_str == '' or pd.isna(back_camera_str):
        return 0
    
    mega_pixels_list = str(back_camera_str).split()
    for item in mega_pixels_list:
        nums = [c for c in item if c.isdigit()]
        if nums:
            mega_pixels_sum += int(''.join(nums))
    return mega_pixels_sum

def clean_price_format(price_str):
    # Check for comma used as decimal separator (like "USD 396,22")
    if ',' in price_str and len(price_str.split(',')[1]) == 2:
        # Replace comma with dot for decimal
        return price_str.replace(',', '.')
    return price_str

df = pd.read_csv("/Users/shivvinnybhutani/LocalShiv/Projects/DE_zoom_camp/week_1_basics_n_setup/2_Docker_Sql/Mobiles Dataset (2025).csv",encoding= "latin1")

df = df[~df["Launched Price (USA)"].str.contains("Not available", na=False)]
df = df[~df["Launched Price (Pakistan)"].str.contains("Not available", na=False)]
df = df[~df["Launched Price (India)"].str.contains("Not available", na=False)]
df = df[~df["Launched Price (China)"].str.contains("Not available", na=False)]
df = df[~df["Launched Price (Dubai)"].str.contains("Not available", na=False)]

df["Launched Price (USA)"] = df["Launched Price (USA)"].apply(clean_price_format)
df["Launched Price (Pakistan)"] = df["Launched Price (Pakistan)"].apply(clean_price_format)
df["Launched Price (India)"] = df["Launched Price (India)"].apply(clean_price_format)
df["Launched Price (China)"] = df["Launched Price (China)"].apply(clean_price_format)
df["Launched Price (Dubai)"] = df["Launched Price (Dubai)"].apply(clean_price_format)

df = df.rename(columns={"Mobile Weight":"Mobile Weight(g)" , "RAM" : "RAM(GB)", "Front Camera":"Front Camera(MP)",
                        "Back Camera" : "Back Camera(MP)(Total)", "Battery Capacity" : "Battery Capacity(mAh)",
                        "Screen Size" : "Screen Size(inches)", "Launched Price (Pakistan)" : "Launched Price(Pakistan)(PKR)",
                        "Launched Price (India)" : "Launched Price(India)(INR)", "Launched Price (China)" : "Launched Price(China)(CNY)",
                        "Launched Price (USA)" : "Launched Price(USA)(USD)", "Launched Price (Dubai)" : "Lanuched Price(Dubai)(AED)"
                        })




#Organize the frame so that appropriate values are numerics
df["Mobile Weight(g)"] = df["Mobile Weight(g)"].str[0:3].astype(int)
df["RAM(GB)"] = df["RAM(GB)"].str[0:1].astype(int)
df["Front Camera(MP)"] = df["Front Camera(MP)"].apply(lambda x: ''.join([c for c in str(x).split()[0] if c.isdigit()])).astype(int)
df["Back Camera(MP)(Total)"] = df["Back Camera(MP)(Total)"].apply(lambda x: get_back_camera_mp_sum(x))
df["Battery Capacity(mAh)"] = df["Battery Capacity(mAh)"].apply(lambda x :''.join([c for c in str(x) if c.isdigit()])).astype(int)
df["Launched Price(Pakistan)(PKR)"] = df["Launched Price(Pakistan)(PKR)"].apply(lambda x: ''.join([c for c in str(x) if c.isdigit()])).astype(int)
df["Launched Price(India)(INR)"] = df["Launched Price(India)(INR)"].apply(lambda x: ''.join([c for c in str(x) if c.isdigit()])).astype(int)
df["Launched Price(China)(CNY)"] = df["Launched Price(China)(CNY)"].apply(lambda x: ''.join([c for c in str(x) if c.isdigit()])).astype(int)
df["Launched Price(USA)(USD)"] = df["Launched Price(USA)(USD)"].apply(lambda x: ''.join([c for c in str(x).split(".")[0] if c.isdigit()])).astype(int)
df["Lanuched Price(Dubai)(AED)"] = df["Lanuched Price(Dubai)(AED)"].apply(lambda x: ''.join([c for c in str(x) if c.isdigit()])).astype(int)
df["Screen Size(inches)"] = df["Screen Size(inches)"].apply(lambda x: ''.join([c for c in str(x).split(',')[0].split('(')[0].strip() if (c.isdigit() or c == ".")])).astype(float)


html = df.to_html()
with open('data_preview.html', 'w') as f:
    f.write(html)
print(f"HTML preview saved to 'data_preview.html'")
print(pd.io.sql.get_schema(df,name = "mobiles_data"))
