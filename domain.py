shipping = {
    2024010101: [
        {"orderNo": 2024010101, "orderSeq": 0, "productNo":123, "deliveryStatus":"PROCESSING"},
        {"orderNo": 2024010101, "orderSeq": 1, "productNo":234, "deliveryStatus":"IN_DELIVERY"}
    ], 
    2024010201: [
        {"orderNo": 2024010201, "orderSeq": 0, "productNo":345, "deliveryStatus":"DELIVERED"},
        {"orderNo": 2024010201, "orderSeq": 1, "productNo":456, "deliveryStatus":"PROCESSING"}
    ]
}

products = {
    123 : {"productNo":123, "productName":"아이폰 16 Pro", "productStatus": "NORMAL"},
    234 : {"productNo":234, "productName":"코카콜라 30캔", "productStatus": "OUT_OF_STOCK"},
    345 : {"productNo":345, "productName":"프링글스 오리지널", "productStatus": "NORMAL"},
    456 : {"productNo":456, "productName":"패캠전자 노트북", "productStatus": "OUT_OF_STOCK"}
}

orders = {
    2024010101: {"orderNo": 2024010101, "orderStatus": "PROCESSING", "totalAmount": 50000,
                 "orderlist": [
                     {"productNo":123, "amount": 20000}, 
                     {"productNo":234, "amount": 30000}
                 ]},
    2024010201: {"orderNo": 2024010201, "orderStatus": "CANCELLED", "totalAmount": 100000,
                 "orderlist": [
                     {"productNo":345, "amount": 30000}, 
                     {"productNo":456, "amount": 70000}
                 ]}
}

