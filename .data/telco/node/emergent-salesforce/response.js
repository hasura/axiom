const mockGetResponse = (requestData) => {
  const demoData = {
    record: {
      attributes: {
        type: 'SBQQ__Quote__c',
        url: '/services/data/v41.0/sobjects/SBQQ__Quote__c/a0p610000040iumAAA'
      },
      Id: 'a0p610000040iumAAA',
      Name: 'Q-00880',
      sbqq__TotalAmount__c: 300,
      sbqq__EffectiveDate__c: '2024-01-01',
      sbqq__ExpirationDate__c: '2024-12-31'
    },
    nextKey: 5,
    netTotal: 300,
    netNonSegmentTotal: 300,
    lineItems: [
      {
        Id: 'a0l61000003u09UAAQ',
        sbqq__ProductId__c: 'a0l61000003p10ABBA',
        sbqq__Product__c: 'Basic Connect',
        sbqq__ProductName__c: 'Unlimited voice calls and 500MB data per month.',
        sbqq__Quantity__c: 1,
        sbqq__UnitPrice__c: 29.99,
        sbqq__DeviceId__c: 'a0l61000003p51NHNA',
        sbqq__Device__c: 'Samsung Galaxy Note 20'
      },
      {
        Id: 'a0l61000003u09UABR',
        sbqq__ProductId__c: 'a0l61000003p12JRRG',
        sbqq__Product__c: 'Traveler\'s Choice',
        sbqq__ProductName__c: 'International roaming package with reduced call and data rates.',
        sbqq__Quantity__c: 1,
        sbqq__UnitPrice__c: 44.99,
        sbqq__DeviceId__c: 'a0l61000003p23PPYU',
        sbqq__Device__c: 'Huawei P50 Pro'
      }
    ]
  };

  return demoData;
};


const mockPostResponse = (requestData) => {
  console.log(requestData);
  let netTotal = '';
  let customerTotal = '';
  switch (requestData.input.dealId) {
    case 'a0l61000003u09UAAQ':
      customerTotal = netTotal = 29.99;
      break;
    case 'a0l61000003u09UABR':
      customerTotal = netTotal = 49.99;
      break;
    default:
      break;
  }
  const orderNumber = 'ORDER' + Array.from({length: 5}, () => 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'.charAt(Math.floor(Math.random() * 62))).join('');

  return {
    record: {
      attributes: {
        type: "Quote",
        url: "/services/data/v60.0/sobjects/Quote/" + requestData.input.dealId
      },
      Name: requestData.input.buyer,
      Id: requestData.input.dealId
    },
    orderConfirmation: {
      orderId: orderNumber,
      orderStatus: "Processing"
    },
    nextKey: null,
    netTotal: netTotal,
    customerTotal: customerTotal
  };
};

export { mockGetResponse, mockPostResponse };
