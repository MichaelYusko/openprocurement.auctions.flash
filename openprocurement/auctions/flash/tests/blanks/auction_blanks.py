# -*- coding: utf-8 -*-

# AuctionAuctionResourceTest


def post_auction_auction(self):
    self.app.authorization = ('Basic', ('auction', ''))
    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': {}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can't report auction results in current (active.tendering) auction status")

    self.set_status('active.auction')

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': {'bids': [{'invalid_field': 'invalid_value'}]}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'], [
        {u'description': {u'invalid_field': u'Rogue field'}, u'location': u'body', u'name': u'bids'}
    ])

    patch_data = {
        'bids': [
            {
                "id": self.initial_bids[1]['id'],
                "value": {
                    "amount": 419,
                    "currency": "UAH",
                    "valueAddedTaxIncluded": True
                }
            }
        ]
    }

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': patch_data}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Number of auction results did not match the number of auction bids")

    patch_data['bids'].append({
        "value": {
            "amount": 409,
            "currency": "UAH",
            "valueAddedTaxIncluded": True
        }
    })

    patch_data['bids'][1]['id'] = "some_id"

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': patch_data}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], {u'id': [u'Hash value is wrong length.']})

    patch_data['bids'][1]['id'] = "00000000000000000000000000000000"

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': patch_data}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Auction bids should be identical to the auction bids")

    patch_data['bids'][1]['id'] = self.initial_bids[0]['id']

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': patch_data})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    auction = response.json['data']
    self.assertNotEqual(auction["bids"][0]['value']['amount'], self.initial_bids[0]['value']['amount'])
    self.assertNotEqual(auction["bids"][1]['value']['amount'], self.initial_bids[1]['value']['amount'])
    self.assertEqual(auction["bids"][0]['value']['amount'], patch_data["bids"][1]['value']['amount'])
    self.assertEqual(auction["bids"][1]['value']['amount'], patch_data["bids"][0]['value']['amount'])
    self.assertEqual('active.qualification', auction["status"])
    self.assertIn("tenderers", auction["bids"][0])
    self.assertIn("name", auction["bids"][0]["tenderers"][0])
    # self.assertIn(auction["awards"][0]["id"], response.headers['Location'])
    self.assertEqual(auction["awards"][0]['bid_id'], patch_data["bids"][0]['id'])
    self.assertEqual(auction["awards"][0]['value']['amount'], patch_data["bids"][0]['value']['amount'])
    self.assertEqual(auction["awards"][0]['suppliers'], self.initial_bids[0]['tenderers'])

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': patch_data}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can't report auction results in current (active.qualification) auction status")

# AuctionLotAuctionResourceTest


def post_auction_auction_lot(self):
    self.app.authorization = ('Basic', ('auction', ''))
    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': {}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can't report auction results in current (active.tendering) auction status")

    self.set_status('active.auction')

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': {'bids': [{'invalid_field': 'invalid_value'}]}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'], [
        {u'description': {u'invalid_field': u'Rogue field'}, u'location': u'body', u'name': u'bids'}
    ])

    patch_data = {
        'bids': [
            {
                "id": self.initial_bids[1]['id'],
                'lotValues': [
                    {
                        "value": {
                            "amount": 419,
                            "currency": "UAH",
                            "valueAddedTaxIncluded": True
                        }
                    }
                ]
            }
        ]
    }

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': patch_data}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Number of auction results did not match the number of auction bids")

    patch_data['bids'].append({
        'lotValues': [
            {
                "value": {
                    "amount": 409,
                    "currency": "UAH",
                    "valueAddedTaxIncluded": True
                }
            }
        ]
    })

    patch_data['bids'][1]['id'] = "some_id"

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': patch_data}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], {u'id': [u'Hash value is wrong length.']})

    patch_data['bids'][1]['id'] = "00000000000000000000000000000000"

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': patch_data}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Auction bids should be identical to the auction bids")

    patch_data['bids'][1]['id'] = self.initial_bids[0]['id']

    for lot in self.initial_lots:
        response = self.app.post_json('/auctions/{}/auction/{}'.format(self.auction_id, lot['id']), {'data': patch_data})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        auction = response.json['data']

    self.assertNotEqual(auction["bids"][0]['lotValues'][0]['value']['amount'], self.initial_bids[0]['lotValues'][0]['value']['amount'])
    self.assertNotEqual(auction["bids"][1]['lotValues'][0]['value']['amount'], self.initial_bids[1]['lotValues'][0]['value']['amount'])
    self.assertEqual(auction["bids"][0]['lotValues'][0]['value']['amount'], patch_data["bids"][1]['lotValues'][0]['value']['amount'])
    self.assertEqual(auction["bids"][1]['lotValues'][0]['value']['amount'], patch_data["bids"][0]['lotValues'][0]['value']['amount'])
    self.assertEqual('active.qualification', auction["status"])
    self.assertIn("tenderers", auction["bids"][0])
    self.assertIn("name", auction["bids"][0]["tenderers"][0])
    # self.assertIn(auction["awards"][0]["id"], response.headers['Location'])
    self.assertEqual(auction["awards"][0]['bid_id'], patch_data["bids"][0]['id'])
    self.assertEqual(auction["awards"][0]['value']['amount'], patch_data["bids"][0]['lotValues'][0]['value']['amount'])
    self.assertEqual(auction["awards"][0]['suppliers'], self.initial_bids[0]['tenderers'])

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': patch_data}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can't report auction results in current (active.qualification) auction status")

# AuctionMultipleLotAuctionResourceTest


def post_auction_auction_2_lot(self):
    self.app.authorization = ('Basic', ('auction', ''))
    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': {}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can't report auction results in current (active.tendering) auction status")

    self.set_status('active.auction')

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': {'bids': [{'invalid_field': 'invalid_value'}]}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'], [
        {u'description': {u'invalid_field': u'Rogue field'}, u'location': u'body', u'name': u'bids'}
    ])

    patch_data = {
        'bids': [
            {
                "id": self.initial_bids[1]['id'],
                'lotValues': [
                    {
                        "value": {
                            "amount": 419,
                            "currency": "UAH",
                            "valueAddedTaxIncluded": True
                        }
                    }
                ]
            }
        ]
    }

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': patch_data}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Number of auction results did not match the number of auction bids")

    patch_data['bids'].append({
        'lotValues': [
            {
                "value": {
                    "amount": 409,
                    "currency": "UAH",
                    "valueAddedTaxIncluded": True
                }
            }
        ]
    })

    patch_data['bids'][1]['id'] = "some_id"

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': patch_data}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], {u'id': [u'Hash value is wrong length.']})

    patch_data['bids'][1]['id'] = "00000000000000000000000000000000"

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': patch_data}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Auction bids should be identical to the auction bids")

    patch_data['bids'][1]['id'] = self.initial_bids[0]['id']

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': patch_data}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], [{"lotValues": ["Number of lots of auction results did not match the number of auction lots"]}])

    for bid in patch_data['bids']:
        bid['lotValues'] = [bid['lotValues'][0].copy() for i in self.initial_lots]

    patch_data['bids'][0]['lotValues'][1]['relatedLot'] = self.initial_bids[0]['lotValues'][0]['relatedLot']

    response = self.app.patch_json('/auctions/{}/auction'.format(self.auction_id), {'data': patch_data}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], [{u'lotValues': [{u'relatedLot': [u'relatedLot should be one of lots of bid']}]}])

    patch_data['bids'][0]['lotValues'][1]['relatedLot'] = self.initial_bids[0]['lotValues'][1]['relatedLot']

    for lot in self.initial_lots:
        response = self.app.post_json('/auctions/{}/auction/{}'.format(self.auction_id, lot['id']), {'data': patch_data})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        auction = response.json['data']

    self.assertNotEqual(auction["bids"][0]['lotValues'][0]['value']['amount'], self.initial_bids[0]['lotValues'][0]['value']['amount'])
    self.assertNotEqual(auction["bids"][1]['lotValues'][0]['value']['amount'], self.initial_bids[1]['lotValues'][0]['value']['amount'])
    self.assertEqual(auction["bids"][0]['lotValues'][0]['value']['amount'], patch_data["bids"][1]['lotValues'][0]['value']['amount'])
    self.assertEqual(auction["bids"][1]['lotValues'][0]['value']['amount'], patch_data["bids"][0]['lotValues'][0]['value']['amount'])
    self.assertEqual('active.qualification', auction["status"])
    self.assertIn("tenderers", auction["bids"][0])
    self.assertIn("name", auction["bids"][0]["tenderers"][0])
    # self.assertIn(auction["awards"][0]["id"], response.headers['Location'])
    self.assertEqual(auction["awards"][0]['bid_id'], patch_data["bids"][0]['id'])
    self.assertEqual(auction["awards"][0]['value']['amount'], patch_data["bids"][0]['lotValues'][0]['value']['amount'])
    self.assertEqual(auction["awards"][0]['suppliers'], self.initial_bids[0]['tenderers'])

    response = self.app.post_json('/auctions/{}/auction'.format(self.auction_id), {'data': patch_data}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can't report auction results in current (active.qualification) auction status")
