import random
import json

def create_data():
    name = ['iPad Air','iPad pro 10.5', 'iPad pro 11','iPad pro 12.9',
            'iPhone 11','iPhone X','iPhone XsMax','iPhone XR',
            'Laptop1','Laptop2','淡黄色长裙']
    # userId random
    type_list = [['Phone','Pad','Computer','Accessories','EarPhone','Other'],
                    ['Apple','Android','Desktop','Laptop','Pen','Wireless','Wired'],
                    ['Windows','Mac','Noiseless','Noise']]
    # withAccessories random
    acc = ['Pen','Charger','Mouse','KeyBoard']
    color = ['green','black','sliver']
    outlook = ['全新','9新','破烂']
    memory = ['8G','16G','32G']
    storage = ['64G','128G','512G']
    pf = ['vx','qq','xy']
    buyer = ['张三','李四','王五']
    ct = ['123456','18812348765','10086']
    # money random
    note = ''

    lucky_number = random.randint(1,10)
    userId = lucky_number

    lucky_number = random.randint(1,len(name)-1)
    productName = name[lucky_number]

    productType = []
    for i in range(3):
        lucky_number = random.randint(1,len(type_list[i])-1)
        ptype = type_list[i][lucky_number]
        productType.append(ptype)

    withAccessories = random.randint(0,1)
    accessories = []
    if withAccessories == 1:
        accessories.append(acc[random.randint(1,len(acc))-1])

    lucky_number = random.randint(0,2)
    productDescription={
        "color":color[lucky_number],
        "outlook":outlook[lucky_number],
        "memory":memory[lucky_number],
        "storage":storage[lucky_number]
    }
    imcome = random.randint(1000,2000)
    sold = random.randint(1500,2500)
    post = random.randint(10,50)
    money = {
        "purchasePrice": imcome,
        "soldPrice":sold,
        "postPrice":post
    }
    lucky_number = random.randint(1,len(pf)-1)
    platform = pf[lucky_number]
    lucky_number = random.randint(1, len(buyer)-1)
    purchaser = buyer[lucky_number]
    lucky_number = random.randint(1, len(ct)-1)
    contact = ct[lucky_number]

    order = {
        "productName":productName,
        "productType":productType,
        "productDescription":productDescription,
        "withAccessories":withAccessories,
        "accessories":accessories,
        "platform":platform,
        "purchaser":purchaser,
        "contact":contact,
        "money":money,
        "note":note
    }
    json_data = {
        "userId": userId,
        "order": order
    }

    return json.dumps(json_data)

# if __name__ == '__main__':
#     print(type(eval(create_data())))





