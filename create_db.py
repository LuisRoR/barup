from models import db
db.drop_all()
db.create_all()
#INSERT INTO Product(brand, name, bottle_weight, vintage, label_name, country, volume,category, description)
INSERT INTO Product VALUES ('Johnnie Walker', 'Black Label', 1400, 2000,'jw_black.jpeg','GB','standard','spirit','Created using only whiskies aged for a minimum of 12 years from the four corners of Scotland, Johnnie Walker Black Label has an unmistakably smooth, deep character.');
